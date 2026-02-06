from app.logic.declarative_rules import RULES_KB, Condition
from collections import Counter

class InquiryEngine:
    def __init__(self):
        self.rules = RULES_KB # Assuming declarative_rules.py defines RULES_KB
        # Map consequences to rules for backward lookup
        self.rule_map = {}
        for rule in self.rules:
            # key: ("derived_fact", "systemic_illness")
            key = rule.consequence
            if key not in self.rule_map:
                self.rule_map[key] = []
            self.rule_map[key].append(rule)

    def get_next_question(self, facts_db):
        """
        Determines the next best leaf symptom to ask.
        """
        patient = "current_patient"
        
        # 1. Identify Candidate Diagnoses Rules
        # Filter for rules that produce 'possible_diagnosis'
        candidates = []
        for rule in self.rules:
            if rule.consequence[0] == "possible_diagnosis":
                # Check if this rule is viable (no contradictions)
                missing = self._scan_rule(rule, facts_db, patient, set())
                if missing is not None: # Not None means viable
                    candidates.extend(missing)
        
        if not candidates:
            return None
            
        # 2. Heuristic: Frequency
        counts = Counter(candidates)
        if not counts:
            return None
            
        return counts.most_common(1)[0][0]

    def _scan_rule(self, rule, facts_db, patient, visited):
        """
        Returns list of missing leaf symptoms if rule is viable.
        Returns None if rule is contradicted.
        """
        missing_leafs = []
        
        for cond in rule.conditions:
            p = cond.predicate
            o = cond.object_val
            target_truth = cond.truth_value
            
            # --- Check Local Knowledge ---
            # Is factor definitively known?
            is_true = facts_db.exists(p, patient, o)
            # For 'not_has_symptom', check negation
            # Simplification: Assume 'not_has_symptom' predicate stores explicit NO
            is_false = False
            if p == "has_symptom":
                 is_false = facts_db.exists("not_has_symptom", patient, o)
            elif p == "derived_fact":
                 # Derived fact false if ALL paths to it are false... complex.
                 # For now, assume derived fact false only if explicitly marked (rare).
                 pass

            # --- Evaluation ---
            if target_truth: # WE NEED TRUE
                if is_false: return None # Contradiction
                if is_true: continue # Satisfied logic locally
                
                # Unknown... is it a leaf or derived?
                if p == "has_symptom":
                    missing_leafs.append(o)
                elif p == "derived_fact":
                    # Expands Derived Fact
                    # Need ANY rule to be viable (OR logic for derivation sources)
                    sub_rules = self.rule_map.get((p, o), [])
                    any_viable = False
                    sub_missing = []
                    
                    for sub_r in sub_rules:
                        if sub_r in visited: continue # Cycle prevention
                        res = self._scan_rule(sub_r, facts_db, patient, visited | {sub_r})
                        if res is not None:
                            any_viable = True
                            sub_missing.extend(res)
                    
                    if not any_viable: return None # Cannot derive necessary fact
                    missing_leafs.extend(sub_missing)

            else: # WE NEED FALSE (e.g. NOT Fever)
                if is_true: return None # Contradiction (Have Fever)
                if is_false: continue # Satisfied (Have No Fever)
                
                # Unknown... leaf?
                if p == "has_symptom":
                    # Asking "Do you have fever?" -> "No" satisfies this.
                    missing_leafs.append(o)
                # Derived facts negation is hard... skip for MVP.
        
        return missing_leafs
