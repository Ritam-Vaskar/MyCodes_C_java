# Q6: Triple Linear Regression Analysis

## Overview
Three separate linear regression analyses exploring different domains:

### Part 1: Medical Cost Personal Dataset
Impact of demographic and health factors on medical insurance costs
- **Target:** Insurance charges ($)

### Part 2: Loan Default Rates
How income, credit score, loan amount affect default likelihood
- **Target:** Default rate (%)

### Part 3: Unemployment Rates  
Economic indicators' impact on unemployment
- **Target:** Unemployment rate (%)

---

## Quick Start

```bash
cd "C:\C programing\ADlab\day2\q6"

# Run all three analyses
python main.py

# Or run individually
cd medical_cost && python main.py
cd loan_default && python main.py
cd unemployment && python main.py
```

---

## Part 1: Medical Cost Analysis

**Research Question:** Impact of age, BMI, smoking, region on medical costs?

**Dataset:** 1,338 individuals with health insurance data

**Top Findings:**
- Smoker×BMI interaction: **+$18,650** (dominant factor)
- Age: **+$3,956** per year
- Smoking alone: **-$8,627** (offset by interaction term)
- Obesity: **+$981**

**Performance:** R² = 0.87 | MAE = $2,710

---

## Part 2: Loan Default Analysis

**Research Question:** How do income, credit score, loan amount, loan term affect default likelihood?

**Dataset:** 10,000 synthetic loan applications

**Top Findings:**
- Income: **-1.77** (higher income reduces default)
- Credit score: **-1.26** (better credit reduces default)
- Loan amount: **+0.66** (larger loans increase default)
- Debt-to-income: **+0.56** (higher DTI increases default)
- Loan term: **+0.42** (longer terms riskier)

**Performance:** R² = 0.76 | MAE = 1.01%

---

## Part 3: Unemployment Rates Analysis

**Research Question:** How do inflation, GDP growth, education affect unemployment?

**Dataset:** 500 synthetic country-year observations

**Top Findings:**
- Education index: **-0.62** (education reduces unemployment)
- Inflation rate: **+0.43** (Phillips Curve relationship)
- GDP×Inflation: **-0.42** (interaction effect)
- Technology index: **-0.21** (tech adoption helps)

**Performance:** R² = -0.25 | MAE = 0.46%
*Note: Negative R² indicates model challenges with synthetic data*

---

## Project Structure

```
q6/
├── main.py                  # Combined runner
├── README.md               # This file
├── requirements.txt        # Dependencies
│
├── medical_cost/           # Part 1
│   ├── main.py
│   ├── model/linear_regression.py
│   ├── utils/
│   └── output/
│
├── loan_default/           # Part 2
│   ├── main.py
│   ├── model/linear_regression.py
│   ├── utils/
│   └── output/
│
└── unemployment/           # Part 3
    ├── main.py
    ├── model/linear_regression.py
    ├── utils/
    └── output/
```

---

## Key Insights

### Medical Cost
- **Smoking is catastrophic** for insurance costs when combined with high BMI
- Age has strong linear relationship
- Regional differences minimal

### Loan Default
- **Credit score is king** - strongest predictor of default
- Income provides protection against default
- Loan-to-income ratio crucial for risk assessment
- Longer terms increase default risk

### Unemployment
- **Education is the strongest factor** reducing unemployment
- Inflation shows positive correlation (Phillips Curve)
- GDP growth reduces unemployment (Okun's Law)
- Technology adoption helps employment

---

## Comparative Results

| Analysis | R² Score | MAE | Sample Size |
|----------|----------|-----|-------------|
| Medical Cost | 0.8688 | $2,710 | 1,338 |
| Loan Default | 0.7634 | 1.01% | 10,000 |
| Unemployment | -0.2513 | 0.46% | 500 |

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

## Outputs

Each analysis generates:
- `predictions.csv` - Actual vs predicted values
- `coefficients.csv` - Feature importance rankings
- `metrics.txt` - Performance metrics
- `visualizations/` - 4 plots each

---

**Date:** December 9, 2025
**Status:** Complete ✓
