"""
Phase 2 — Data Loading
------------------------
Groceries dataset: each line = one transaction (comma-separated items).
No InvoiceNo column, no cancellations/negative quantities to remove —
already transaction-level and pre-cleaned.

Phase 3 — Transaction Encoding
--------------------------------
One-hot encode the cleaned transactions into a (transactions x items)
boolean matrix using mlxtend's TransactionEncoder.
"""
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder


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


def encode_transactions(
    transactions: list[list[str]], min_item_freq: int = 0
) -> pd.DataFrame:
    """
    One-hot encode transactions into a (transactions x items) boolean matrix.

    min_item_freq: optional — drop items appearing in fewer than this many
    transactions, to reduce noise/sparsity. 0 = keep all items (default).
    """
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_array, columns=te.columns_)

    if min_item_freq > 0:
        item_counts = df.sum(axis=0)
        keep_cols = item_counts[item_counts >= min_item_freq].index
        df = df[keep_cols]

    return df


if __name__ == "__main__":
    txns = clean_transactions(load_transactions())
    basket_df = encode_transactions(txns)
    print(f"Transactions: {len(txns)}")
    print(f"Encoded matrix shape (transactions x items): {basket_df.shape}")
    print(basket_df.head())
    basket_df.to_pickle("outputs/basket_encoded.pkl")
