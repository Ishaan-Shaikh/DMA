import itertools
import time
import tracemalloc
import random
from collections import defaultdict

def generate_dataset(num_transactions=10000, num_items=100):
    """Generates a synthetic dataset with embedded frequent patterns."""
    dataset = []
    patterns = [
        ["Item_1", "Item_2", "Item_3", "Item_4", "Item_5"],
        ["Item_10", "Item_11", "Item_12", "Item_13"],
        ["Item_20", "Item_21", "Item_22"]
    ]
    for _ in range(num_transactions):
        transaction = set()
        for pattern in patterns:
            if random.random() < 0.20: # 20% chance to include a pattern
                transaction.update(random.sample(pattern, random.randint(2, len(pattern))))
        while len(transaction) < 10:
            transaction.add(f"Item_{random.randint(30, num_items)}")
        dataset.append(frozenset(transaction))
    return dataset

def apriori_original(dataset, min_support_count):
    # ... (Standard Apriori Implementation) ...
    # Counts support against the FULL dataset at every iteration k.
    pass # (Full code provided in experimental setup)

def apriori_transaction_reduction(dataset, min_support_count):
    """Modified Apriori with Transaction Reduction (ATR)."""
    # Step 1: Find frequent 1-itemsets (same as original)
    item_counts = defaultdict(int)
    for transaction in dataset:
        for item in transaction:
            item_counts[item] += 1
    
    L1 = {frozenset([item]): count for item, count in item_counts.items() if count >= min_support_count}
    L = [L1]
    k = 2
    
    # MODIFICATION: Initialize reduced dataset
    reduced_dataset = dataset
    candidate_counts_history = []
    reduced_dataset_sizes = [len(dataset)]
    
    while True:
        prev_L = list(L[-1].keys())
        Ck = set()
        # Join and Prune Step
        for i in range(len(prev_L)):
            for j in range(i + 1, len(prev_L)):
                union = prev_L[i].union(prev_L[j])
                if len(union) == k:
                    subsets = [frozenset(union - set([item])) for item in union]
                    if all(subset in L[-1] for subset in subsets):
                        Ck.add(union)
        
        if not Ck:
            break
        candidate_counts_history.append(len(Ck))
        
        ck_counts = {}
        new_reduced_dataset = []
        
        # MODIFICATION: Count support AND filter dataset simultaneously
        for transaction in reduced_dataset:
            has_frequent_k = False
            for candidate in Ck:
                if candidate.issubset(transaction):
                    ck_counts[candidate] = ck_counts.get(candidate, 0) + 1
                    has_frequent_k = True
            
            # Keep transaction only if it contributes to a frequent k-itemset
            if has_frequent_k:
                new_reduced_dataset.append(transaction)
                
        Lk = {candidate: count for candidate, count in ck_counts.items() if count >= min_support_count}
        if not Lk:
            break
            
        L.append(Lk)
        reduced_dataset = new_reduced_dataset
        reduced_dataset_sizes.append(len(reduced_dataset))
        k += 1
        
    return L, candidate_counts_history, reduced_dataset_sizes
