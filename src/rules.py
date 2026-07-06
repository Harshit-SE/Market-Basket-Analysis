"""
Phase 5 — Association Rule Generation
----------------------------------------
Rules generated from the FP-Growth itemsets (identical to Apriori's,
just faster to produce — documented in Phase 4).
"""
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules

MIN_SUPPORT = 0.01
MIN_CONFIDENCE = 0.3
MIN_LIFT = 1.0  # lift > 1 required for a "meaningful" association


def generate_rules(
    basket_df: pd.DataFrame,
    min_support: float = MIN_SUPPORT,
    min_confidence: float = MIN_CONFIDENCE,
    min_lift: float = MIN_LIFT,
) -> pd.DataFrame:
    itemsets = fpgrowth(basket_df, min_support=min_support, use_colnames=True)
    rules = association_rules(itemsets, metric="confidence", min_threshold=min_confidence)
    rules = rules[rules["lift"] >= min_lift]
    rules = rules.sort_values("lift", ascending=False).reset_index(drop=True)

    # readable string form instead of frozenset repr
    rules["antecedents_str"] = rules["antecedents"].apply(lambda s: ", ".join(sorted(s)))
    rules["consequents_str"] = rules["consequents"].apply(lambda s: ", ".join(sorted(s)))
    return rules


if __name__ == "__main__":
    basket_df = pd.read_pickle("outputs/basket_encoded.pkl")
    rules = generate_rules(basket_df)

    print(f"Rules generated (confidence >= {MIN_CONFIDENCE}, lift >= {MIN_LIFT}): {len(rules)}")
    cols = ["antecedents_str", "consequents_str", "support", "confidence", "lift"]
    print(rules[cols].head(10).to_string(index=False))

    export_df = rules[cols].rename(
        columns={"antecedents_str": "antecedents", "consequents_str": "consequents"}
    )
    export_df.to_csv("outputs/association_rules.csv", index=False)
    rules.to_pickle("outputs/rules_full.pkl")
    print("\nSaved: outputs/association_rules.csv, outputs/rules_full.pkl")
