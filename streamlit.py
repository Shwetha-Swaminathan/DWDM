  import streamlit as st
from itertools import combinations

class Apriori:
    def __init__(self, min_support=0.5, min_confidence=0.5):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.transactions = []

    def load_data(self, dataset):
        self.transactions = dataset

    def _get_itemsets(self, items, k):
        return list(combinations(items, k))

    def _get_frequent_itemsets(self, itemsets):
        freq_itemsets = {}
        for transaction in self.transactions:
            for itemset in itemsets:
                if set(itemset).issubset(transaction):
                    freq_itemsets[itemset] = freq_itemsets.get(itemset, 0) + 1
        return {itemset: support for itemset, support in freq_itemsets.items() if support >= self.min_support * len(self.transactions)}

    def _get_association_rules(self, freq_itemsets):
        rules = []
        for itemset, support in freq_itemsets.items():
            if len(itemset) > 1:
                for i in range(1, len(itemset)):
                    for antecedent in combinations(itemset, i):
                        consequent = tuple(item for item in itemset if item not in antecedent)
                        confidence = support / freq_itemsets[antecedent]
                        if confidence >= self.min_confidence:
                            rules.append((antecedent, consequent, confidence))
        return rules

    def find_frequent_itemsets(self):
        frequent_itemsets = {}
        k = 1
        while True:
            itemsets = self._get_itemsets(set(item for transaction in self.transactions for item in transaction), k)
            freq_itemsets = self._get_frequent_itemsets(itemsets)
            if not freq_itemsets:
                break
            frequent_itemsets.update(freq_itemsets)
            k += 1
        return frequent_itemsets

    def find_association_rules(self):
        frequent_itemsets = self.find_frequent_itemsets()
        return self._get_association_rules(frequent_itemsets)

def main():
    st.title("Apriori Algorithm for Association Rule Mining")

    dataset = st.text_area("Enter your dataset (each transaction on a new line):", value=
    """
    bread, milk
    bread, diaper, beer, egg
    milk, diaper, beer, cola
    bread, milk, diaper, beer
    bread, milk, diaper, cola
    """)

    transactions = [set(line.strip().split(', ')) for line in dataset.split('\n') if line.strip()]
    
    min_support = st.slider("Minimum Support", min_value=0.1, max_value=1.0, step=0.1, value=0.5)
    min_confidence = st.slider("Minimum Confidence", min_value=0.1, max_value=1.0, step=0.1, value=0.5)

    apriori = Apriori(min_support=min_support, min_confidence=min_confidence)
    apriori.load_data(transactions)

    frequent_itemsets = apriori.find_frequent_itemsets()
    st.subheader("Frequent Itemsets:")
    for itemset, support in frequent_itemsets.items():
        st.write(f"{itemset}: {support}")

    association_rules = apriori.find_association_rules()
    st.subheader("Association Rules:")
    for rule in association_rules:
        st.write(f"{rule[0]} => {rule[1]}  Confidence: {rule[2]}")

if __name__ == "__main__":
    main()
