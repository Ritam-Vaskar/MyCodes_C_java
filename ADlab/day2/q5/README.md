# Q5: Dual Linear Regression Analysis

## Overview
This project contains two separate linear regression analyses exploring different real-world applications:

### Part 1: Car Mileage Prediction
**Research Question:** What is the impact of engine size, weight, horsepower, and fuel type on car mileage?
- **Dataset:** Auto MPG Dataset (UCI Repository)
- **Target Variable:** Miles Per Gallon (MPG)

### Part 2: Health Insurance Charges Analysis
**Research Question:** How do variables like age, BMI, gender, smoking habits, and region affect health insurance charges?
- **Dataset:** Health Insurance Dataset
- **Target Variable:** Insurance Charges ($)

---

## Project Structure

```
q5/
├── main.py                          # Combined runner for both analyses
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
│
├── car_mileage/                     # Part 1: Car Mileage Prediction
│   ├── main.py                      # Main analysis script
│   ├── model/
│   │   └── linear_regression.py    # MPGPredictor class
│   ├── utils/
│   │   ├── data_loader.py          # Data loading & preprocessing
│   │   └── evaluation.py           # Evaluation & visualization
│   └── output/                      # Results (predictions, metrics, plots)
│       └── visualizations/
│
└── insurance_charges/               # Part 2: Insurance Charges
    ├── main.py                      # Main analysis script
    ├── model/
    │   └── linear_regression.py    # InsuranceChargesPredictor class
    ├── utils/
    │   ├── data_loader.py          # Data loading & preprocessing
    │   └── evaluation.py           # Evaluation & visualization
    └── output/                      # Results (predictions, metrics, plots)
        └── visualizations/
```

---

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup
```bash
cd "C:\C programing\ADlab\day2\q5"
pip install -r requirements.txt
```

---

## Usage

### Option 1: Run Both Analyses (Recommended)
```bash
python main.py
```
This will run both analyses sequentially with prompts between them.

### Option 2: Run Individual Analyses

**Car Mileage Only:**
```bash
cd car_mileage
python main.py
```

**Insurance Charges Only:**
```bash
cd insurance_charges
python main.py
```

---

## Part 1: Car Mileage Prediction

### Research Question
**What is the impact of engine size, weight, horsepower, and fuel type on car mileage?**

### Dataset
- **Source:** UCI ML Repository - Auto MPG Dataset
- **Samples:** ~398 cars
- **Features:** 
  - Numerical: displacement, horsepower, weight, acceleration
  - Categorical: cylinders (4/6/8), origin (USA/Europe/Japan)
  - Target: MPG (9-47 range)

### Key Features Analyzed
1. **Engine Size (displacement):** Total engine volume
2. **Weight:** Car weight in pounds
3. **Horsepower:** Engine power output
4. **Fuel Type/Origin:** Car origin as proxy for fuel efficiency standards
5. **Cylinders:** Number of engine cylinders
6. **Power-to-weight ratio:** Derived feature

### Expected Findings
- **Negative Correlations:** Weight, horsepower, displacement decrease MPG
- **Positive Correlations:** Newer model years, Japanese origin increase MPG
- **R² Score:** 0.75-0.85 (Strong predictive power)
- **MAE:** 2-3 MPG

### Output Files
- `predictions.csv`: Actual vs predicted MPG
- `coefficients.csv`: Feature importance rankings
- `metrics.txt`: Performance metrics
- `visualizations/`: 4 plots (predictions, residuals, features, correlation)

---

## Part 2: Health Insurance Charges Analysis

### Research Question
**How do variables like age, BMI, gender, smoking habits, and region affect health insurance charges?**

### Dataset
- **Samples:** ~1,338 individuals
- **Features:**
  - Demographics: age, gender
  - Health: BMI, number of children
  - Lifestyle: smoking status
  - Geographic: region (4 US regions)
  - Target: Insurance charges ($1,000-$65,000)

### Key Features Analyzed
1. **Age:** Older individuals → higher charges
2. **BMI:** Body Mass Index (health indicator)
3. **Smoking Status:** Expected to be strongest predictor
4. **Gender:** Male vs Female
5. **Children:** Number of dependents
6. **Region:** Geographic cost variations
7. **Interaction Features:** smoker_bmi, age_bmi

### Expected Findings
- **Smoking:** Strongest positive impact (~$20,000+ increase)
- **Age:** Strong positive correlation ($200-300 per year)
- **BMI:** Moderate positive impact (obesity increases costs)
- **R² Score:** 0.70-0.80
- **MAE:** $3,000-$5,000

### Output Files
- `predictions.csv`: Actual vs predicted charges
- `coefficients.csv`: Feature importance rankings
- `metrics.txt`: Performance metrics
- `visualizations/`: 4 plots (predictions, residuals, features, correlation)

---

## Methodology

### 1. Data Loading & Preprocessing
- Load datasets from online repositories (with fallback to synthetic data)
- Handle missing values
- Encode categorical variables (binary & one-hot encoding)
- Create derived features

### 2. Feature Engineering
- **Car Mileage:** Power-to-weight ratio, displacement per cylinder
- **Insurance:** BMI categories, age groups, interaction terms

### 3. Model Training
- Algorithm: Linear Regression with StandardScaler normalization
- Split: 80% training, 20% testing
- Random state: 42 (reproducibility)

### 4. Evaluation
- **R² Score:** Proportion of variance explained
- **MAE:** Average absolute prediction error
- **RMSE:** Root mean squared error
- **MAPE:** Mean absolute percentage error

### 5. Visualization
- Actual vs Predicted scatter plots
- Residual analysis
- Feature importance bar charts
- Correlation heatmaps

---

## Key Insights

### Car Mileage Analysis
**Primary Factors Affecting MPG:**
1. **Weight** (-): Heavier cars consume more fuel
2. **Horsepower** (-): More powerful engines less efficient
3. **Displacement** (-): Larger engines burn more fuel
4. **Model Year** (+): Newer cars more efficient due to technology
5. **Origin** (+): Japanese cars historically more fuel-efficient

**Practical Applications:**
- Automotive design optimization
- Fuel efficiency predictions for consumers
- Environmental impact assessment
- Policy-making for fuel economy standards

### Insurance Charges Analysis
**Primary Factors Affecting Charges:**
1. **Smoking Status** (+): Dominant factor (health risk)
2. **Age** (+): Older individuals higher medical costs
3. **BMI** (+): Obesity-related health complications
4. **Children** (+): Dependent coverage costs
5. **Region** (±): Geographic cost variations

**Practical Applications:**
- Premium calculation models
- Risk assessment for insurance companies
- Health policy recommendations
- Personalized health insurance counseling

---

## Comparison of Both Analyses

| Aspect | Car Mileage | Insurance Charges |
|--------|-------------|-------------------|
| **Domain** | Automotive | Healthcare |
| **Prediction Type** | Efficiency (MPG) | Cost ($) |
| **Sample Size** | ~398 | ~1,338 |
| **Features** | 12-14 | 13-15 |
| **Expected R²** | 0.75-0.85 | 0.70-0.80 |
| **Key Factor** | Weight | Smoking |
| **Strongest Impact** | Physical attributes | Behavioral factors |

---

## Requirements

```
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
```

---

## Future Enhancements

### Car Mileage
- Non-linear models (Polynomial Regression, Random Forest)
- Time series analysis for technology improvements
- Electric vehicle MPG equivalent (MPGe) analysis

### Insurance Charges
- Feature interactions (smoker × age, BMI × age)
- Clustering analysis for risk groups
- Incorporation of medical history data

### Both Analyses
- Cross-validation for robust performance estimates
- Regularization (Lasso, Ridge) for feature selection
- Interactive dashboards for predictions

---

## References

### Datasets
1. **Auto MPG Dataset:** Quinlan, R. (1993). UCI Machine Learning Repository.
   https://archive.ics.uci.edu/ml/datasets/Auto+MPG

2. **Insurance Dataset:** Stedy Machine Learning with R Datasets.
   https://github.com/stedy/Machine-Learning-with-R-datasets

### Methodology
- Scikit-learn Documentation: https://scikit-learn.org/
- Linear Regression Theory: James et al. (2013). "An Introduction to Statistical Learning"

---

## License
Educational project for Advanced Data Analytics Lab coursework.

---

## Contact
For questions or suggestions, please refer to the course repository.

---

**Last Updated:** December 2025
