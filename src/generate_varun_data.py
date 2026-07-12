"""
Synthetic transaction generator — Varun Beverages (PepsiCo bottling partner, India)
--------------------------------------------------------------------------------------
Simulates retail outlet restocking orders. Each transaction = one outlet's
order, containing a basket of SKUs from Varun Beverages' actual PepsiCo
portfolio (colas, flavoured CSDs, energy, juice, water).

Association patterns are hand-designed to mirror real distribution behavior:
- Aquafina (water) is a near-universal add-on, like a staple.
- Pepsi + Mountain Dew are frequently ordered together (flagship colas, same outlets).
- Mirinda Orange + Mirinda Lemon are ordered together (brand-family restocking).
- Sting (energy) skews toward Mountain Dew outlets (youth/energy positioning).
- Tropicana + Slice are ordered together (juice category restocking).
- 7Up + Nimbooz cluster together (lemon-flavour family).
- Gatorade is a smaller, semi-independent category (sports retail channel).
"""
import random

random.seed(42)

PRODUCTS = [
    "Pepsi", "Diet Pepsi", "Mountain Dew", "7Up", "Mirinda Orange", "Mirinda Lemon",
    "Sting", "Tropicana", "Slice", "Aquafina", "Nimbooz", "Gatorade",
]

# baseline probability an item appears in a random transaction (drives "top sellers")
BASE_PROB = {
    "Pepsi": 0.42,
    "Aquafina": 0.55,
    "Mountain Dew": 0.30,
    "7Up": 0.28,
    "Mirinda Orange": 0.22,
    "Mirinda Lemon": 0.18,
    "Sting": 0.20,
    "Diet Pepsi": 0.12,
    "Tropicana": 0.16,
    "Slice": 0.14,
    "Nimbooz": 0.10,
    "Gatorade": 0.08,
}

# co-purchase lift rules: if item on the left is present, boost prob of item on the right
CO_PURCHASE_BOOST = [
    ("Pepsi", "Mountain Dew", 0.35),
    ("Mountain Dew", "Sting", 0.40),
    ("Mirinda Orange", "Mirinda Lemon", 0.50),
    ("Tropicana", "Slice", 0.45),
    ("7Up", "Nimbooz", 0.42),
    ("Pepsi", "Aquafina", 0.25),
    ("Mountain Dew", "Aquafina", 0.25),
    ("Sting", "Aquafina", 0.20),
]


def generate_transaction() -> list[str]:
    basket = set()
    for product, prob in BASE_PROB.items():
        if random.random() < prob:
            basket.add(product)

    # apply co-purchase boosts (a second pass so ordering doesn't matter)
    for trigger, target, boost in CO_PURCHASE_BOOST:
        if trigger in basket and target not in basket:
            if random.random() < boost:
                basket.add(target)

    if not basket:  # avoid empty transactions
        basket.add(random.choice(PRODUCTS))

    return list(basket)


def generate_dataset(n_transactions: int = 8000) -> list[list[str]]:
    return [generate_transaction() for _ in range(n_transactions)]


if __name__ == "__main__":
    transactions = generate_dataset(8000)
    with open("data/varun_beverages.csv", "w") as f:
        for t in transactions:
            f.write(",".join(t) + "\n")

    sizes = [len(t) for t in transactions]
    print(f"Transactions written: {len(transactions)}")
    print(f"Unique products: {len(PRODUCTS)}")
    print(f"Basket size — min: {min(sizes)}, max: {max(sizes)}, mean: {sum(sizes)/len(sizes):.2f}")
