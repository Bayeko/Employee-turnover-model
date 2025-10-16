Zonla Turnover — Final Model

Rank-constrained decision tree with m-estimate smoothing and out-of-fold (OOF) isotonic calibration.
Temporal outer CV across years (2019→2022 train, test on 2020/2021/2022), inner repeated CV (3×5) with 1-SE rule, final refit on 2019–2022 and scoring the active 2023 cohort (to predict 2024).

1) Project Structure
.
├─ turnover_decisiontree_finalversion.py   # main script (training, CV, final scoring)
├─ scripts/
│  └─ download_data.sh                     # optional helper to fetch sample data
└─ data/                                   # (optional) put CSVs here or in CWD

2) Data Requirements

Provide yearly snapshots with these exact filenames (current working directory or data/):

employee_information_2019.csv
employee_information_2020.csv
employee_information_2021.csv
employee_information_2022.csv
employee_information_2023.csv


Minimum expected fields (case/space tolerant — the script normalizes headers):
unique_id, record_date, work_location, voluntary_termination_count plus HR attributes used as features:
tenure_group/tenure_company_ratio, years_in_position, months_since_last_promotion,
hierarchy_level, is_people_manager, fte, age_group,
highest_performance_rating, bravo_award, high_potential,
recruitment_source, five_dynamics_personality.

Notes
• The code auto-detecte numérique vs. catégoriel et crée des flags “*_is_missing” pour les numériques.
• gender est exclu par design pour la soumission.
• La cible “leave in t+1” est dérivée via appariement t→t+1 et un proxy voluntary_term (map de voluntary_termination_count).

Optional: download helper
./scripts/download_data.sh [DEST_DIR]   # default: ~/Downloads


Sinon, copie manuelle des employee_information_*.csv dans le répertoire du script ou ./data.

3) How to Run
# Option A: depuis le dossier contenant les CSV
python turnover_decisiontree_finalversion.py

# Option B: si tes CSV sont dans ./data, lance depuis le repo racine
(cd data && python ../turnover_decisiontree_finalversion.py)

Python & deps

Python ≥ 3.9

numpy, pandas, scikit-learn, matplotlib

Instal rapide :

pip install -r requirements.txt
# ou
pip install numpy pandas scikit-learn matplotlib

4) What the script does

Verify & load employee_information_2019..2023.csv

Build labels: pour chaque employé, dernier enregistrement de l’année t → cible = a quitté volontairement en t+1.

Preprocess: imputation (median/most_frequent), One-Hot (drop='first'), rangs métiers (features “débloquées” selon la profondeur).

Model: arbre contraint par rang + m-estimate smoothing au niveau des feuilles.

Model selection: inner CV 3×5, grille compacte (max_depth ∈ {7,8,9}, min_leaf ∈ {40,60,80,120}, m_shrink ∈ {min_leaf/2, min_leaf, 2*min_leaf}), règle 1-SE.

Outer temporal CV: test 2020/2021/2022 (train ≤ année-1).

Métriques: AUC individuel, RMSE des moyennes prédites par site (pondéré & non-pondéré).

OOF isotonic calibration sur l’ensemble d’entraînement outer (zéro fuite).

Final refit: sur 2019–2022 avec params agrégés (vote), OOF iso calibrator refitté.

Predict 2023 active (exclut ceux déjà terminés en 2023) → risque 2024.

Save artifacts.

5) Outputs

decision_tree_readable.txt — impression textuelle de l’arbre final (features transformées).

turnover_probability_distribution.png — histogramme des probabilités individuelles.

individual_turnover_probabilities_sorted.csv — (unique_id, turnover_probability), trié décroissant.

avg_turnover_by_location_sorted.csv — (work_location, predicted_avg_turnover_rate) en %.

6) Results (Lonza 2025 Challenge)

Q1 — Average turnover by location (2024)

RMSE: 0.089

Rank: 19 / 31

(Référence: médiane 0.077, meilleur 0.053)

Q2 — Individual voluntary turnover probability (2024)

AUC: 0.679

Rank: 12 / 22

(Référence: aléatoire 0.5, meilleur 0.792)

Les courbes ROC et détails officiels proviennent de l’évaluation du challenge interne (Erwan & Maike, session du 8 oct).

7) Modeling Notes

Rank gating (ordre métier) pour encourager des splits interprétables:
0) tenure/ancienneté & mouvement, 1) niveau hiérarchie & people manager,
2) site & FTE & âge, 3) performance & bravo/high-potential, 4+) recrutement & personnalité.

m-estimate: lissage bayésien des feuilles (prior = moyenne d’entraînement, force liée à min_leaf).

Isotonic OOF: calibration monotone en dehors de l’échantillon d’entraînement pour des probabilités mieux calibrées.

1-SE rule: privilégie le modèle plus simple dont la perf est dans l’intervalle d’une erreur standard du meilleur.

8) Repro & Troubleshooting

Fichiers manquants → le script s’arrête et liste ceux à fournir.

Colonnes absentes → elles sont ignorées; garde la nomenclature indiquée plus haut pour maximiser l’info.

Versions: fixe RANDOM_STATE=42; des diffs mineurs peuvent subsister selon versions libs.

Sites non présents en 2023 → pas de moyenne par site créée.
