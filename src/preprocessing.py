"""
Phase 2 — Data Loading
------------------------
Groceries dataset: each line = one transaction (comma-separated items).
No InvoiceNo column, no cancellations/negative quantities to remove —
already transaction-level and pre-cleaned.
"""


def load_transactions(path: str = "data/groceries.csv") -> list[list[str]]:
    """Load raw basket data as a list of transactions (list of item lists)."""
    transactions = []
    with open(path, "r") as f:
        for line in f:
            items = [item.strip() for item in line.strip().split(",") if item.strip()]
            if items:
                transactions.append(items)
    return transactions


def clean_transactions(transactions: list[list[str]]) -> list[list[str]]:
    """Remove duplicate items within the same basket, drop any empty rows."""
    cleaned = []
    for t in transactions:
        deduped = list(dict.fromkeys(t))  # preserves order, drops dup items
        if deduped:
            cleaned.append(deduped)
    return cleaned
