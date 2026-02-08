class Facts():
    def __init__(self):
        self.facts = set()
    
    def add_fact(self, predicate, subject, object_val):
        self.facts.add((predicate, subject, object_val))

    def add_facts(self, facts_list):
        for f in facts_list:
            self.facts.add(f)
    
    def get_facts(self):
        return list(self.facts)
    
    def query(self, predicate=None, subject=None, object_val=None):
        
        results = []
        for fact in self.facts:
            p, s, o = fact
            if predicate is not None and p != predicate:
                continue
            if subject is not None and s != subject:
                continue
            if object_val is not None and o != object_val:
                continue
            results.append(fact)
        return results

    def exists(self, predicate, subject, object_val):
        return (predicate, subject, object_val) in self.facts