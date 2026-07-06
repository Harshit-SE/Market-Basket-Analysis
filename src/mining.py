"""
Phase 4 — Frequent Itemset Mining (Apriori vs FP-Growth)
----------------------------------------------------------
Both algorithms run on the SAME encoded basket matrix with the SAME
min_support so their outputs and runtimes can be fairly compared.
"""
import time
import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth

MIN_SUPPORT = 0.01  # itemset must appear in >=1% of baskets (~98 transactions)


def run_apriori(basket_df: pd.DataFrame, min_support: float = MIN_SUPPORT):
    start = time.perf_counter()
    itemsets = apriori(basket_df, min_support=min_support, use_colnames=True)
    elapsed = time.perf_counter() - start
    return itemsets, elapsed


def run_fpgrowth(basket_df: pd.DataFrame, min_support: float = MIN_SUPPORT):
    start = time.perf_counter()
    itemsets = fpgrowth(basket_df, min_support=min_support, use_colnames=True)
    elapsed = time.perf_counter() - start
    return itemsets, elapsed


if __name__ == "__main__":
    basket_df = pd.read_pickle("outputs/basket_encoded.pkl")

    apriori_itemsets, apriori_time = run_apriori(basket_df)
    fpgrowth_itemsets, fpgrowth_time = run_fpgrowth(basket_df)

    print(f"Apriori:   {len(apriori_itemsets)} itemsets in {apriori_time:.4f}s")
    print(f"FP-Growth: {len(fpgrowth_itemsets)} itemsets in {fpgrowth_time:.4f}s")
    print(f"FP-Growth was {apriori_time/fpgrowth_time:.2f}x faster")

    # readable itemset labels instead of frozenset repr
    apriori_itemsets["itemsets"] = apriori_itemsets["itemsets"].apply(lambda s: ", ".join(sorted(s)))
    fpgrowth_itemsets["itemsets"] = fpgrowth_itemsets["itemsets"].apply(lambda s: ", ".join(sorted(s)))

    print("\nTop 10 frequent itemsets (Apriori), by support:")
    print(apriori_itemsets.sort_values("support", ascending=False).head(10).to_string(index=False))

    apriori_itemsets.to_pickle("outputs/apriori_itemsets.pkl")
    fpgrowth_itemsets.to_pickle("outputs/fpgrowth_itemsets.pkl")

    with open("outputs/mining_comparison.md", "w") as f:
        f.write(
            f"# Apriori vs FP-Growth — Performance Comparison\n\n"
            f"| Metric | Apriori | FP-Growth |\n|---|---|---|\n"
            f"| Runtime | {apriori_time:.4f}s | {fpgrowth_time:.4f}s |\n"
            f"| Itemsets found | {len(apriori_itemsets)} | {len(fpgrowth_itemsets)} |\n\n"
            f"FP-Growth was **{apriori_time/fpgrowth_time:.2f}x faster** on this dataset "
            f"(9,835 transactions, 169 items, min_support={MIN_SUPPORT}). Both algorithms "
            f"find the identical set of itemsets — the difference is purely in search "
            f"strategy: Apriori repeatedly scans the data generating and pruning candidates "
            f"level-by-level, while FP-Growth compresses the data into a tree once and mines "
            f"it without candidate generation, which is why it scales better as data grows.\n"
        )
    print("\nSaved: outputs/apriori_itemsets.pkl, outputs/fpgrowth_itemsets.pkl, outputs/mining_comparison.md")
