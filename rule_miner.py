import itertools
import pandas as pd

class RuleMiner(object):

    def __init__(self, support_t, confidence_t):
        self.support_t = support_t
        self.confidence_t = confidence_t 

    def get_support(self, data, itemset):
        curr_itemset = data[itemset].all(axis=1)
        support =  curr_itemset.sum()
        return support

    def merge_itemsets(self, itemsets):
        if not itemsets:
            return []

        new_itemsets = set()
        k = len(itemsets[0])

        # Corrected loop: starts from 0 instead of i+1
        for i in range(len(itemsets)):
            for j in range(i+1, len(itemsets)):
                combined_itemset = list(set(itemsets[i]) | set(itemsets[j]))
                combined_itemset.sort()

                if len(combined_itemset) == k + 1:
                    new_itemsets.add(tuple(combined_itemset))

        return [list(itemset) for itemset in new_itemsets]



    def get_rules(self, itemset):
    
        rules = []
        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = list(antecedent)
                consequent = list(set(itemset) - set(antecedent))
                rules.append([antecedent, consequent])
        return rules


    def get_frequent_itemsets(self, data):
    
        itemsets = [[i] for i in data.columns]
        freq_itemsets = []

        while itemsets:
            new_itemsets = []
            for itemset in itemsets:
                
                if self.get_support(data, itemset) >= self.support_t:
                    freq_itemsets.append(itemset)
                    new_itemsets.append(itemset)

            itemsets = self.merge_itemsets(new_itemsets) if new_itemsets else []
        
        return freq_itemsets


    def get_confidence(self, data, rule):
        
        X = rule[0]
        Y = rule[1]

        support_X = self.get_support(data, X)
        support_XY = self.get_support(data, X + Y)

        if support_X == 0:
            return 0.0
        else:
            confidence = support_XY / support_X
            return confidence


    def get_association_rules(self, data):

        itemsets = self.get_frequent_itemsets(data)
        rules = []
        
        for itemset in itemsets:

            if len(itemset) > 1:
                itemset_rules = self.get_rules(itemset)
                rules.extend(itemset_rules)

        
        association_rules = []
        for rule in rules:
            
            confidence = self.get_confidence(data, rule)
            if(confidence >= self.confidence_t):
                association_rules.append(rule)

        return association_rules
