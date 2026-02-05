from app.logic.rules import Rules
from app.logic.facts import Facts

import inspect

class Inference():
    
    def __init__(self):
        self.rules = [m[1] for m in inspect.getmembers(Rules, inspect.isfunction)]

    def infer(self, facts_instance):
        found_diagnoses = []
        
        # Iterative Forward Chaining (Fixed Point)
        # We loop until no new facts are derived.
        while True:
            new_facts_added = False
            
            for rule in self.rules:
                # Rules yield tuples like ("diagnosis", "User", "dengue")
                results = rule(facts_instance)
                if results:
                    for res in results:
                        # If simple diagnosis, we just track it
                        # If it's an intermediate fact/warning, we add it back to DB
                        predicate, subject, object_val = res
                        
                        # Check existance to avoid infinite loops or duplicates
                        if not facts_instance.exists(predicate, subject, object_val):
                            facts_instance.add_fact(predicate, subject, object_val)
                            new_facts_added = True
                            
                            # Log valid output
                            if predicate == "diagnosis" or predicate == "warning" or predicate == "alert" or predicate == "risk":
                                found_diagnoses.append(res)
            
            if not new_facts_added:
                break
        
        # Deduplicate results
        return list(set(found_diagnoses))

