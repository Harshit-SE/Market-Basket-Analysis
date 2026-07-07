# Apriori vs FP-Growth — Performance Comparison

| Metric | Apriori | FP-Growth |
|---|---|---|
| Runtime | 0.1387s | 0.1981s |
| Itemsets found | 333 | 333 |

FP-Growth was **0.70x faster** on this dataset (9,835 transactions, 169 items, min_support=0.01). Both algorithms find the identical set of itemsets — the difference is purely in search strategy: Apriori repeatedly scans the data generating and pruning candidates level-by-level, while FP-Growth compresses the data into a tree once and mines it without candidate generation, which is why it scales better as data grows.
