
import json
import os
import re

class SymptomParser:
    def __init__(self):
        # Determine the path to symptoms.json relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level (to 'app') then into 'data'
        data_path = os.path.join(current_dir, '..', 'data', 'symptoms.json')
        
        try:
            with open(data_path, 'r') as f:
                self.symptoms_list = json.load(f)
        except Exception as e:
            print(f"Error loading symptoms: {e}")
            self.symptoms_list = []

        # Create a mapping dictionary for easier lookups
        # e.g. "stiff neck" -> "stiff_neck"
        self.symptom_map = {s.replace('_', ' '): s for s in self.symptoms_list}
        # Also map original form just in case
        for s in self.symptoms_list:
            self.symptom_map[s] = s

    def extract_symptoms(self, text: str):
        """
        Extracts known symptoms from the text.
        Returns a dictionary with 'present' and 'absent' lists.
        """
        text = text.lower()
        found_present = []
        found_absent = []

        # Simple keyword matching
        # Sort keys by length descending to match "severe headache" before "headache"
        sorted_keys = sorted(self.symptom_map.keys(), key=len, reverse=True)

        for phrase in sorted_keys:
            # Check if the phrase exists in the text as a whole word
            # Using regex boundary \b to ensure we match whole words
            pattern = re.compile(r'\b' + re.escape(phrase) + r'\b')
            locations = [m.start() for m in pattern.finditer(text)]
            
            if locations:
                # Check for negation: look at words immediately preceding the match
                # Simple negation check: look for "no", "not", "without" in the preceding few words
                is_negated = False
                for loc in locations:
                    # Look back up to 20 chars
                    prefix = text[max(0, loc-20):loc]
                    if re.search(r'\b(no|not|without|neither|nor)\b', prefix):
                        is_negated = True
                        break # Assume if negated once, it's negated (simple logic)
                
                symptom_id = self.symptom_map[phrase]
                
                if is_negated:
                    if symptom_id not in found_absent and symptom_id not in found_present:
                        found_absent.append(symptom_id)
                else:
                    if symptom_id not in found_present and symptom_id not in found_absent:
                        found_present.append(symptom_id)

        return {
            "present": found_present,
            "absent": found_absent
        }
