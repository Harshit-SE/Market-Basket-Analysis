# Project Tracker — Market Basket Analysis

> Status legend: ⬜ Not Started · 🟨 In Progress · ✅ Done

This tracker breaks the project into small, incremental, testable features. Each step builds on the previous one. Anyone (human or AI) opening this file should immediately understand **what's done, what's next, and what depends on what.**

---

## Progress Snapshot

| Phase | Status | % Complete |
|---|---|---|
| Phase 1: Setup | ⬜ | 0% |
| Phase 2: Data & EDA | ⬜ | 0% |
| Phase 3: Transaction Encoding | ⬜ | 0% |
| Phase 4: Frequent Itemset Mining | ⬜ | 0% |
| Phase 5: Association Rule Generation | ⬜ | 0% |
| Phase 6: Visualization & Insights | ⬜ | 0% |
| Phase 7 (Optional): Deployment | ⬜ | 0% |

---

## Phase 1 — Project Setup
- [ ] Create project folder structure (`data/`, `notebooks/`, `src/`, `outputs/`)
- [ ] Set up virtual environment / install dependencies (`mlxtend`, `pandas`, `networkx`)
- [ ] Download Online Retail (or Groceries) dataset into `data/`
- [ ] Create `market_basket_analysis.ipynb` notebook skeleton

**Depends on:** nothing (first step)
**Unlocks:** Phase 2

---

## Phase 2 — Data Loading & EDA
- [ ] Load dataset with pandas, inspect shape/dtypes/nulls
- [ ] Remove cancelled orders / negative quantities / nulls
- [ ] Identify top 10–20 best-selling items
- [ ] Analyze basket size distribution (items per transaction)
- [ ] Explore time-based trends (if timestamp available — e.g. by month/day)
- [ ] Summarize 3–5 key purchase patterns found (write in notebook markdown)

**Depends on:** Phase 1
**Unlocks:** Phase 3
**Output artifact:** EDA charts + written findings in notebook

---

## Phase 3 — Transaction Encoding
- [ ] Group raw rows by transaction/invoice ID into item lists
- [ ] Convert transaction list into one-hot encoded basket matrix using `TransactionEncoder` (mlxtend)
- [ ] Filter out extremely rare items (optional, to reduce noise/sparsity)
- [ ] Verify encoded matrix shape (transactions × unique items)

**Depends on:** Phase 2
**Unlocks:** Phase 4
**Output artifact:** One-hot encoded transaction DataFrame

---

## Phase 4 — Frequent Itemset Mining
- [ ] Run **Apriori** algorithm with a chosen `min_support` threshold
- [ ] Run **FP-Growth** algorithm with the same `min_support` threshold
- [ ] Compare runtime/performance of Apriori vs FP-Growth
- [ ] Inspect top frequent itemsets from each method

**Depends on:** Phase 3
**Unlocks:** Phase 5
**Output artifact:** Frequent itemsets table (from both algorithms)

---

## Phase 5 — Association Rule Generation
- [ ] Generate rules using `association_rules()` (mlxtend) from frequent itemsets
- [ ] Set thresholds for Confidence and Lift to filter meaningful rules
- [ ] Sort rules by Lift (strongest associations first)
- [ ] Save final rule set to `outputs/association_rules.csv`

**Depends on:** Phase 4
**Unlocks:** Phase 6
**Output artifact:** `association_rules.csv` with Support/Confidence/Lift columns

---

## Phase 6 — Visualization & Business Insights
- [ ] Bar chart: Top 10 frequent itemsets by support
- [ ] Scatter plot: Support vs Confidence (bubble size = Lift)
- [ ] Network graph of item-to-item associations (networkx)
- [ ] Write plain-English business recommendations from top rules
      (e.g. "Bundle Item A + Item B — 70% of Item A buyers also buy Item B")
- [ ] Add final insights summary to README/notebook

**Depends on:** Phase 5
**Unlocks:** Phase 7 (optional) or Project Complete
**Output artifact:** Visualizations + written business insight report

---

## Phase 7 — Optional: Deployment / Demo
- [ ] Build simple Streamlit app to explore rules interactively
- [ ] Add dropdown to select a product and view its top associated products
- [ ] Display rule metrics (support/confidence/lift) in-app
- [ ] Deploy locally or on Streamlit Community Cloud

**Depends on:** Phase 6
**Unlocks:** N/A (stretch goal)

---

## Change Log
| Date | Change | By |
|---|---|---|
| _(fill in)_ | Project initialized, README + Tracker created | — |

---

## Notes for future contributors (human or AI)
- Always update the checkbox **and** the Progress Snapshot % when a task is completed.
- If a step is blocked, mark it 🟨 and add a one-line reason next to it.
- Keep business insights in plain English — the value of this project is in actionable recommendations, not just raw metrics.
- If dataset is large, consider sampling for Apriori (it scales worse than FP-Growth on large itemsets).
