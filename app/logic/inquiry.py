from app.logic.declarative_rules import RULES_KB, Condition
from collections import Counter

class InquiryEngine:
    def __init__(self):
        self.rules = RULES_KB
        self.rule_map = {}
        for rule in self.rules:
            key = rule.consequence
            if key not in self.rule_map:
                self.rule_map[key] = []
            self.rule_map[key].append(rule)

    def get_next_question(self, facts_db):
        patient = "current_patient"
        
        candidates = []
        for rule in self.rules:
            if rule.consequence[0] == "possible_diagnosis":
                missing = self._scan_rule(rule, facts_db, patient, set())
                if missing is not None:
                    candidates.extend(missing)
        
        if not candidates:
            return None
            
        counts = Counter(candidates)
        if not counts:
            return None
            
        return counts.most_common(1)[0][0]

    def _scan_rule(self, rule, facts_db, patient, visited):
        missing_leafs = []
        
        for cond in rule.conditions:
            p = cond.predicate
            o = cond.object_val
            target_truth = cond.truth_value
            
            is_true = facts_db.exists(p, patient, o)
            is_false = False
            if p == "has_symptom":
                 is_false = facts_db.exists("not_has_symptom", patient, o)
            elif p == "derived_fact":
                 pass

            if target_truth:
                if is_false: return None
                if is_true: continue
                
                if p == "has_symptom":
                    missing_leafs.append(o)
                elif p == "derived_fact":
                    sub_rules = self.rule_map.get((p, o), [])
                    any_viable = False
                    sub_missing = []
                    
                    for sub_r in sub_rules:
                        if sub_r in visited: continue
                        res = self._scan_rule(sub_r, facts_db, patient, visited | {sub_r})
                        if res is not None:
                            any_viable = True
                            sub_missing.extend(res)
                    
                    if not any_viable: return None
                    missing_leafs.extend(sub_missing)

            else:
                if is_true: return None
                if is_false: continue
                
                if p == "has_symptom":
                    missing_leafs.append(o)
        
        return missing_leafs
