# Employee Turnover Prediction — Final Model

> **Rank-constrained decision tree** with *m-estimate smoothing* and *out-of-fold isotonic calibration*.  
> Implements temporal outer cross-validation (year-based) with inner repeated CV (3×5) and the **1-SE rule** for model selection.  
> Final refit on **2019–2022** data and scoring of the **active 2023 cohort** to predict **2024 voluntary turnover**.

![Status](https://img.shields.io/badge/status-final-brightgreen)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-private-lightgrey)

---

## 📁 Project Structure
.
├─ turnover_decisiontree_finalversion.py # main script (training, CV, scoring)
├─ scripts/
│ └─ download_data.sh # optional data helper
└─ data/ # optional folder for CSVs


---

## 📊 Data Requirements

The model expects **five yearly CSV snapshots**:
employee_information_2019.csv
employee_information_2020.csv
employee_information_2021.csv
employee_information_2022.csv
employee_information_2023.csv




### Expected Columns

| Category | Examples |
|-----------|-----------|
| **Identifiers** | `unique_id`, `record_date`, `work_location`, `voluntary_termination_count` |
| **Tenure & Mobility** | `tenure_group` / `tenure_company_ratio`, `years_in_position`, `months_since_last_promotion` |
| **Structure** | `hierarchy_level`, `is_people_manager`, `fte`, `age_group` |
| **Performance** | `highest_performance_rating` / `latest_performance_rating`, `bravo_award`, `high_potential` |
| **Talent / Traits** | `recruitment_source`, `five_dynamics_personality` |

> `gender` is excluded by design.  
> Missing values are imputed; numeric columns get an additional `_is_missing` flag.  
> The binary target is derived from `voluntary_termination_count` (`T` or `1` → terminated).

Optional helper:

./scripts/download_data.sh [DEST_DIR]   # default: ~/Downloads

⚙️ Installation

Python ≥ 3.9

pip install numpy pandas scikit-learn matplotlib
# or
pip install -r requirements.txt



Example requirements.txt:

numpy>=1.24
pandas>=2.0
scikit-learn>=1.3
matplotlib>=3.7

🚀 How to Run

From the folder containing your CSV files:

python turnover_decisiontree_finalversion.py


If files are inside ./data:

(cd data && python ../turnover_decisiontree_finalversion.py)

🧠 Model Overview

Verify & load yearly data.

Build targets: last record per employee per year → label as “1” if voluntarily left in t + 1.

Preprocess: median/mode imputation, One-Hot encoding, and rank-based feature gating.

Model: decision tree with rank constraints and m-estimate smoothing at leaves.

Inner CV (3×5): grid search

max_depth ∈ {7, 8, 9}

min_leaf ∈ {40, 60, 80, 120}

m_shrink ∈ {½·min_leaf, min_leaf, 2·min_leaf}
→ pick the simplest model within one SE of best AUC.

Temporal outer CV: train ≤ year − 1, test on {2020, 2021, 2022}.

Isotonic calibration: out-of-fold (no leakage).

Final refit: on 2019–2022 using aggregated parameters (voting).

Predict active 2023 employees → 2024 turnover risk.

Export results.

📂 Outputs
File	Description
decision_tree_readable.txt	Readable text version of the final tree
turnover_probability_distribution.png	Histogram of predicted probabilities
individual_turnover_probabilities_sorted.csv	Employee-level probabilities (sorted)
avg_turnover_by_location_sorted.csv	Average predicted turnover per site (%)
📈 Example Results
Task	Metric	Example Score	Comment
Predict average turnover by location	RMSE	0.089	Lower = better
Predict individual voluntary turnover	AUC	0.679	0.5 = random · 1.0 = perfect

(Example benchmark values — your results will depend on your data.)

🧩 Modeling Notes

Rank gating: progressively unlocks feature groups by tree depth
(tenure → hierarchy → site → performance → recruitment).

m-estimate smoothing: Bayesian regularization toward global mean.

Out-of-Fold isotonic calibration: monotonic probability correction without data leakage.

1-SE rule: prefers the simplest model within one standard error of the best AUC.

🧰 Troubleshooting

Missing files → script stops and lists required filenames.

Missing columns → safely ignored; complete data improves accuracy.

Minor score variations may appear across scikit-learn versions.

If work_location is missing, per-site averages are skipped.

Random seed fixed at RANDOM_STATE = 42.

⚠️ gender is intentionally excluded for fairness.
Always ensure data governance and privacy compliance before re-using this model.


---

✅ **Instructions:**  
1. Copy everything inside the gray code block above.  
2. Paste it into your `README.md` file.  
3. Commit it — GitHub will automatically render headers, bold text, emojis, and tables perfectly.
