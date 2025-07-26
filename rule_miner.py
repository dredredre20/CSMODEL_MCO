import itertools
import pandas as pd

class RuleMiner(object):

    def __init__(self, support_t, confidence_t):
        self.support_t = support_t
        self.confidence_t = confidence_t 

    # Get the support of an itemset in the dataset
    def get_support(self, data, itemset):
        # Check if itemset is empty or not
        if not itemset:
            return 0

        # Get the specific itemset from the data and calculate its support
        curr_itemset = data[itemset].all(axis=1)
        support =  curr_itemset.sum()
        return support

    # Merge itemsets to create new itemsets of length k+1
    def merge_itemsets(self, itemsets):
        if not itemsets:
            return []

        # create a set to hold new itemsets
        new_itemsets = set()
        k = len(itemsets[0])

        # Iterate through pairs of itemsets and combine them
        for i in range(len(itemsets)):
            for j in range(i+1, len(itemsets)):

                combined_itemset = list(set(itemsets[i]) | set(itemsets[j]))
                combined_itemset.sort()

                # Only add the combined itemset if it has length k+1
                if len(combined_itemset) == k + 1:
                    new_itemsets.add(tuple(combined_itemset))

        # Convert the set of new itemsets back to a list of lists
        return [list(itemset) for itemset in new_itemsets]


    # Generate all possible rules from an itemset
    def get_rules(self, itemset):
    
        rules = []

        # Generate all possible non-empty antecedents
        # and their corresponding consequents
        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = list(antecedent)
                consequent = list(set(itemset) - set(antecedent))
                rules.append([antecedent, consequent])
        return rules


    # Get all frequent itemsets from the dataset
    def get_frequent_itemsets(self, data):
    
        # Initialize itsemsets with the current columns of the data
        itemsets = [[i] for i in data.columns]
        freq_itemsets = []

        # Iterate until no more frequent itemsets can be found
        while itemsets:
            new_itemsets = []
            for itemset in itemsets:
                
                # Check if the itemset meets the support threshold
                # If it does, add it to the list of frequent itemsets
                if self.get_support(data, itemset) >= self.support_t:
                    freq_itemsets.append(itemset)
                    new_itemsets.append(itemset)

            # Generate new itemsets by merging the current frequent itemsets
            itemsets = self.merge_itemsets(new_itemsets) if new_itemsets else []
        
        return freq_itemsets


    # Calculate the confidence of a rule
    def get_confidence(self, data, rule):
        
        # Get the antecedent and consequent of the rule
        X = rule[0]
        Y = rule[1]

        # Calculate the support of the antecedent and the rule
        support_X = self.get_support(data, X)
        support_XY = self.get_support(data, X + Y)

        # If support of antecedent is zero, return confidence as zero
        if support_X == 0:
            return 0.0
        else:
            confidence = support_XY / support_X
            return confidence


    # Get all association rules from the dataset
    def get_association_rules(self, data):

        # Get all frequent itemsets from the data
        itemsets = self.get_frequent_itemsets(data)
        rules = []
        
        # Iterate through each itemset and generate rules
        for itemset in itemsets:

            if len(itemset) > 1:
                itemset_rules = self.get_rules(itemset)
                rules.extend(itemset_rules)

        
        association_rules = []

        # For each rule, calculate the confidence and check if it meets the threshold
        for rule in rules:
            
            confidence = self.get_confidence(data, rule)
            if(confidence >= self.confidence_t):
                association_rules.append(rule)

        return association_rules
