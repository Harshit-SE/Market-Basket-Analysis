"""
Runs the full Market Basket Analysis pipeline on the Varun Beverages
dataset, phase by phase. Outputs go to outputs/varun/ to keep this
separate from the Groceries dataset results.

Usage: python src/main_varun.py   (run from the project root)
"""
from preprocessing import load_transactions, clean_transactions, encode_transactions
from mining import run_apriori, run_fpgrowth
from rules import generate_rules
from visualize import (
    plot_top_itemsets_bar,
    plot_support_confidence_bubble,
    plot_rule_network,
    business_insights,
)
import eda

DATA_PATH = "data/varun_beverages.csv"
OUT_DIR = "outputs/varun"


def main():
    print("=== Phase 2: EDA ===")
    txns = clean_transactions(load_transactions(DATA_PATH))
    top = eda.top_items(txns, n=12)
    stats = eda.basket_size_stats(txns)
    eda.plot_top_items(top, f"{OUT_DIR}/top_items.png")
    eda.plot_basket_size_distribution(stats["sizes"], f"{OUT_DIR}/basket_size_distribution.png")
    print(f"Transactions: {len(txns)}")
    print(f"Top item: {top[0][0]} ({top[0][1]} transactions)")
    print(f"Basket size — mean: {stats['mean']:.2f}, max: {stats['max']}")

    print("\n=== Phase 3: Transaction Encoding ===")
    basket_df = encode_transactions(txns)
    print(f"Encoded matrix shape: {basket_df.shape}")

    print("\n=== Phase 4: Frequent Itemset Mining ===")
    MIN_SUPPORT = 0.03  # lower catalog size (12 items) needs a higher threshold than Groceries
    apriori_itemsets, apriori_time = run_apriori(basket_df, MIN_SUPPORT)
    fpgrowth_itemsets, fpgrowth_time = run_fpgrowth(basket_df, MIN_SUPPORT)
    print(f"Apriori: {len(apriori_itemsets)} itemsets in {apriori_time:.4f}s")
    print(f"FP-Growth: {len(fpgrowth_itemsets)} itemsets in {fpgrowth_time:.4f}s")

    print("\n=== Phase 5: Association Rule Generation ===")
    rules = generate_rules(basket_df, min_support=MIN_SUPPORT, min_confidence=0.3, min_lift=1.0)
    print(f"Rules generated: {len(rules)}")
    export_cols = ["antecedents_str", "consequents_str", "support", "confidence", "lift"]
    rules[export_cols].rename(
        columns={"antecedents_str": "antecedents", "consequents_str": "consequents"}
    ).to_csv(f"{OUT_DIR}/association_rules.csv", index=False)

    print("\n=== Phase 6: Visualization & Insights ===")
    apriori_named = apriori_itemsets.copy()
    apriori_named["itemsets"] = apriori_named["itemsets"].apply(lambda s: ", ".join(sorted(s)))
    plot_top_itemsets_bar(apriori_named, f"{OUT_DIR}/top_itemsets_bar.png")
    plot_support_confidence_bubble(rules, f"{OUT_DIR}/support_confidence_bubble.png")
    plot_rule_network(rules, f"{OUT_DIR}/rule_network.png", top_n=15)

    insights = business_insights(rules)
    with open(f"{OUT_DIR}/business_insights.md", "w") as f:
        f.write(insights)
    print(insights)

    print(f"\nPipeline complete. All outputs written to {OUT_DIR}/")


if __name__ == "__main__":
    main()
