from app.logic.declarative_rules import RULES_KB
from app.logic.facts import Facts

class Inference():
    
    def __init__(self):
        self.rules = RULES_KB

    def infer(self, facts_instance):
        found_diagnoses = []
        patient = "current_patient"
        
        while True:
            new_facts_added = False
            
            for rule in self.rules:
                conditions_met = True
                
                for cond in rule.conditions:
                    p = cond.predicate
                    o = cond.object_val
                    
                    exists = facts_instance.exists(p, patient, o)
                    
                    if cond.truth_value and not exists:
                        conditions_met = False
                        break
                    if not cond.truth_value and exists:
                        conditions_met = False
                        break
                
                if conditions_met:
                    conseq_p, conseq_o = rule.consequence
                    
                    if not facts_instance.exists(conseq_p, patient, conseq_o):
                        facts_instance.add_fact(conseq_p, patient, conseq_o)
                        new_facts_added = True
                        
                        if conseq_p == "possible_diagnosis":
                            found_diagnoses.append((conseq_p, patient, conseq_o))
            
            if not new_facts_added:
                break
        
        return list(set(found_diagnoses))
