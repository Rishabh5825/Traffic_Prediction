# 🚦 Traffic Demand Prediction

> Predicting traffic demand at specific geographic locations and timestamps using a **3-model weighted ensemble** of CatBoost, LightGBM, and XGBoost with extensive spatial feature engineering.

![Python](https://img.shields.io/badge/Python-3.11.9-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![CatBoost](https://img.shields.io/badge/CatBoost-Gradient_Boosting-FFCC00)
![LightGBM](https://img.shields.io/badge/LightGBM-Gradient_Boosting-02569B)
![XGBoost](https://img.shields.io/badge/XGBoost-Gradient_Boosting-EC4E20)

---

## 📋 Problem Statement

Given a dataset with **geohash-encoded locations**, timestamps, road metadata, and weather conditions, predict continuous **traffic demand** values. The evaluation metric is **RMSE** (Root Mean Squared Error).

---

## 🏗️ Project Structure

```
Traffic_Prediction/
├── 01_ensemble_cat_lgb_xgb.ipynb   # Main notebook — full ML pipeline
├── APPROACH.txt                     # Detailed methodology write-up
├── README.md                        # This file
├── .gitignore                       # Git ignore rules
├── train.csv                        # Training data (77,299 rows)
├── test.csv                         # Test data (41,778 rows)
├── prediction.csv                   # Final submission output
└── dataset/
    ├── analyze.py                   # Standalone EDA script
    └── sample_submission.csv        # Expected submission format
```

---

## 🔬 Methodology

### Feature Engineering

| Category | Features | Purpose |
|---|---|---|
| **Spatial (Geohash)** | `latitude`, `longitude` decoded from geohash | Core location features |
| **Geohash Prefixes** | `gh_prefix_3`, `gh_prefix_4`, `gh_prefix_5` | Multi-resolution spatial grouping |
| **Polynomial Spatial** | `lat²`, `lon²`, `lat × lon` | Non-linear spatial patterns |
| **Distance** | `dist_from_center` | Radial demand patterns |
| **KMeans Clusters** | `spatial_cluster` (k=8) | Coarse neighborhood zones |
| **Temporal** | `hour`, `minute`, `time_slot`, `hour_sin/cos`, `is_peak` | Time-of-day & cyclical encoding |
| **Imputation** | RoadType → Residential, Weather → Sunny, Temp → median | Missing value handling |

### Models

| Model | Iterations | Learning Rate | Key Params |
|---|---|---|---|
| **CatBoost** | 2,000 | 0.05 | depth=6, native categoricals |
| **LightGBM** | 2,000 | 0.05 | 127 leaves, feature/bagging fraction=0.8 |
| **XGBoost** | 2,000 | 0.05 | depth=6, subsample=0.8, hist method |

All models use **early stopping** (patience = 100 rounds).

### Ensemble Strategy

- **5-Fold Cross-Validation** (KFold, shuffle=True, seed=42)
- Out-of-fold (OOF) predictions collected across all folds
- **Weighted average ensemble** — weights = inverse of each model's OOF RMSE
- Test predictions averaged across all 5 folds

---

## 📊 Dataset

| Column | Type | Description |
|---|---|---|
| `geohash` | string | 6-character geohash-encoded location |
| `day` | int | Day identifier |
| `timestamp` | string | Time of day (`H:MM` format) |
| `demand` | float | **Target variable** (train only) |
| `RoadType` | categorical | e.g., Residential |
| `NumberofLanes` | int | Number of road lanes |
| `LargeVehicles` | categorical | Allowed / Not Allowed |
| `Landmarks` | categorical | Yes / No |
| `Temperature` | float | Temperature reading |
| `Weather` | categorical | Sunny / Rainy / Snowy |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Jupyter Notebook or JupyterLab

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/Traffic_Prediction.git
cd Traffic_Prediction

# Create a virtual environment
python -m venv venv

# Activate the environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install pandas numpy scikit-learn catboost lightgbm xgboost jupyter
```

### Run the Pipeline

```bash
# Launch Jupyter
jupyter notebook

# Open and run: 01_ensemble_cat_lgb_xgb.ipynb
```

### Quick EDA (optional)

```bash
cd dataset
python analyze.py
```

---

## 📁 Output

The notebook produces **`prediction.csv`** with two columns:

| Column | Description |
|---|---|
| `Index` | Row index matching test.csv |
| `demand` | Predicted traffic demand |

---

## 🛠️ Tech Stack

- **Language:** Python 3.11.9
- **Environment:** Jupyter Notebook
- **Libraries:**
  - `pandas` — Data manipulation
  - `numpy` — Numerical operations
  - `scikit-learn` — KFold, KMeans, LabelEncoder, metrics
  - `catboost` — CatBoostRegressor
  - `lightgbm` — LightGBM training API
  - `xgboost` — XGBRegressor

---

## 📄 License

This project is for academic/educational purposes.

---

## 🤝 Acknowledgments

Built as an MCA project exploring ensemble methods for geospatial traffic demand forecasting.
