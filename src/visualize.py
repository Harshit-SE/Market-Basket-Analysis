"""
Phase 6 — Visualization & Business Insights
----------------------------------------------
Bar chart of top itemsets, support-vs-confidence bubble plot (bubble
size = lift), network graph of item-to-item associations, and
plain-English business recommendations from the top rules.
"""
import matplotlib
matplotlib.use("Agg")  # headless — no display in this environment
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


def plot_top_itemsets_bar(itemsets: pd.DataFrame, out_path: str, n: int = 10):
    top = itemsets.sort_values("support", ascending=False).head(n)
    plt.figure(figsize=(9, 6))
    plt.barh(top["itemsets"][::-1], top["support"][::-1], color="#F18F01")
    plt.xlabel("Support")
    plt.title(f"Top {n} Frequent Itemsets by Support")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_support_confidence_bubble(rules: pd.DataFrame, out_path: str):
    plt.figure(figsize=(9, 6))
    sizes = (rules["lift"] ** 2) * 20  # scale for visibility
    scatter = plt.scatter(
        rules["support"], rules["confidence"], s=sizes,
        c=rules["lift"], cmap="viridis", alpha=0.7, edgecolors="black", linewidths=0.3,
    )
    plt.colorbar(scatter, label="Lift")
    plt.xlabel("Support")
    plt.ylabel("Confidence")
    plt.title("Association Rules: Support vs Confidence (bubble size = Lift)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_rule_network(rules: pd.DataFrame, out_path: str, top_n: int = 20):
    """Network graph of the top-N rules by lift: antecedent -> consequent."""
    top_rules = rules.sort_values("lift", ascending=False).head(top_n)

    G = nx.DiGraph()
    for _, row in top_rules.iterrows():
        for a in row["antecedents"]:
            for c in row["consequents"]:
                G.add_edge(a, c, weight=row["lift"])

    plt.figure(figsize=(11, 9))
    pos = nx.spring_layout(G, k=0.9, seed=42)
    weights = [G[u][v]["weight"] for u, v in G.edges()]

    nx.draw_networkx_nodes(G, pos, node_size=1400, node_color="#2E86AB", alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="white")
    nx.draw_networkx_edges(
        G, pos, width=[w / max(weights) * 4 for w in weights],
        edge_color="#A23B72", arrowsize=15, alpha=0.7,
    )
    plt.title(f"Item Association Network (Top {top_n} Rules by Lift)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def business_insights(rules: pd.DataFrame, n: int = 5) -> str:
    top = rules.sort_values("lift", ascending=False).head(n)
    lines = ["# Business Recommendations\n"]
    for _, row in top.iterrows():
        ante = row["antecedents_str"]
        cons = row["consequents_str"]
        lines.append(
            f"- Customers who buy **{ante}** buy **{cons}** "
            f"{row['confidence']*100:.0f}% of the time (lift {row['lift']:.2f}x baseline) "
            f"-> bundle or shelve these together / recommend {cons} at checkout when {ante} is in the cart."
        )
    return "\n".join(lines)


if __name__ == "__main__":
    apriori_itemsets = pd.read_pickle("outputs/apriori_itemsets.pkl")
    rules = pd.read_pickle("outputs/rules_full.pkl")

    plot_top_itemsets_bar(apriori_itemsets, "outputs/top_itemsets_bar.png")
    plot_support_confidence_bubble(rules, "outputs/support_confidence_bubble.png")
    plot_rule_network(rules, "outputs/rule_network.png")

    insights = business_insights(rules)
    print(insights)
    with open("outputs/business_insights.md", "w") as f:
        f.write(insights)

    print("\nSaved: outputs/top_itemsets_bar.png, outputs/support_confidence_bubble.png, "
          "outputs/rule_network.png, outputs/business_insights.md")
