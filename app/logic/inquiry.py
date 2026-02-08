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
        
        scored_candidates = []
        for rule in self.rules:
            if rule.consequence[0] == "possible_diagnosis":
                res = self._scan_rule(rule, facts_db, patient, set())
                if res:
                    missing, match_count, total_count = res
                    score = match_count / total_count if total_count > 0 else 0
                    scored_candidates.append({
                        "rule": rule.name,
                        "missing": missing,
                        "score": score,
                        "match": match_count,
                        "total": total_count
                    })
        
        if not scored_candidates:
            return None
            
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)
        
        if not scored_candidates:
            return None

        best_score = scored_candidates[0]["score"]
        top_candidates = [c for c in scored_candidates if c["score"] >= best_score - 0.01] 
        
        all_missing = []
        for c in top_candidates:
            all_missing.extend(c["missing"])
            
        if not all_missing:
            return None
            
        counts = Counter(all_missing)
        return counts.most_common(1)[0][0]

    def _scan_rule(self, rule, facts_db, patient, visited):
        missing_leafs = []
        match_count = 0
        total_count = 0
        
        for cond in rule.conditions:
            p = cond.predicate
            o = cond.object_val
            target_truth = cond.truth_value
            
            is_true = facts_db.exists(p, patient, o)
            is_false = False
            if p == "has_symptom":
                 is_false = facts_db.exists("not_has_symptom", patient, o)
            
            if target_truth:
                if is_false: return None
                if is_true: 
                    match_count += 1
                    total_count += 1
                    continue
                
                if p == "has_symptom":
                    missing_leafs.append(o)
                    total_count += 1
                elif p == "derived_fact":
                    sub_rules = self.rule_map.get((p, o), [])
                    best_sub = None
                    
                    for sub_r in sub_rules:
                        if sub_r in visited: continue
                        res = self._scan_rule(sub_r, facts_db, patient, visited | {sub_r})
                        if res:
                            if best_sub is None:
                                best_sub = res
                            else:
                                curr_ratio = best_sub[1]/best_sub[2] if best_sub[2]>0 else 0
                                new_ratio = res[1]/res[2] if res[2]>0 else 0
                                if new_ratio > curr_ratio:
                                    best_sub = res
                    
                    if best_sub is None: return None
                    
                    missing_leafs.extend(best_sub[0])
                    match_count += best_sub[1]
                    total_count += best_sub[2]

            else:
                if is_true: return None
                if is_false:
                    match_count += 1
                    total_count += 1
                    continue
                
                if p == "has_symptom":
                    missing_leafs.append(o)
                    total_count += 1
        
        return missing_leafs, match_count, total_count
