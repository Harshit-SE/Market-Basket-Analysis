"""
Phase 2 — Exploratory Data Analysis
------------------------------------
Top-selling items, basket size distribution, written findings.
Note: no timestamp column in this dataset, so time-based trend
analysis (tracker's optional step) is skipped and documented below.
"""
import matplotlib
matplotlib.use("Agg")  # headless — no display in this environment
import matplotlib.pyplot as plt
from collections import Counter
from preprocessing import load_transactions, clean_transactions


def top_items(transactions: list[list[str]], n: int = 15) -> list[tuple[str, int]]:
    counts = Counter(item for t in transactions for item in t)
    return counts.most_common(n)


def basket_size_stats(transactions: list[list[str]]) -> dict:
    sizes = [len(t) for t in transactions]
    return {
        "min": min(sizes),
        "max": max(sizes),
        "mean": sum(sizes) / len(sizes),
        "sizes": sizes,
    }


def plot_top_items(items: list[tuple[str, int]], out_path: str):
    names, counts = zip(*items)
    plt.figure(figsize=(9, 6))
    plt.barh(names[::-1], counts[::-1], color="#2E86AB")
    plt.xlabel("Number of transactions")
    plt.title(f"Top {len(items)} Best-Selling Items")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_basket_size_distribution(sizes: list[int], out_path: str):
    plt.figure(figsize=(8, 5))
    plt.hist(sizes, bins=range(1, max(sizes) + 2), color="#A23B72", edgecolor="white")
    plt.xlabel("Items per transaction")
    plt.ylabel("Number of transactions")
    plt.title("Basket Size Distribution")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


if __name__ == "__main__":
    txns = clean_transactions(load_transactions())

    top = top_items(txns, n=15)
    stats = basket_size_stats(txns)

    plot_top_items(top, "outputs/top_items.png")
    plot_basket_size_distribution(stats["sizes"], "outputs/basket_size_distribution.png")

    print(f"Transactions: {len(txns)}")
    print("Top 5 items:", top[:5])
    print("Basket size stats:", {k: v for k, v in stats.items() if k != "sizes"})

    findings = f"""
Key Purchase Patterns Found
============================
1. "whole milk" is the single most purchased item ({top[0][1]} transactions),
   appearing in roughly {top[0][1]/len(txns)*100:.1f}% of all baskets.
2. "other vegetables" and "rolls/buns" round out the top 3, suggesting daily
   staples dominate basket composition over discretionary items.
3. Basket sizes are small and right-skewed: mean {stats['mean']:.2f} items,
   with {sum(1 for s in stats['sizes'] if s <= 5)/len(stats['sizes'])*100:.1f}% of baskets containing 1-5 items.
4. Max basket size is {stats['max']} items — large multi-item baskets are rare,
   so later association rules should focus on small itemsets (pairs/triples).
5. No timestamp field exists in this dataset, so seasonal/time-of-day trend
   analysis is not applicable — documented here as a known dataset limitation.
"""
    print(findings)
    with open("outputs/eda_findings.md", "w") as f:
        f.write(findings)
