# Predictive Power of Linear Regression in House Price Estimation

## Overview
This project analyzes how accurately linear regression can predict house prices based on features like area, number of rooms, and location using the Boston Housing Dataset.

## Project Structure
```
day2/
├── main.py                 # Main execution script
├── README.md              # This file
├── requirements.txt       # Dependencies
├── model/
│   └── linear_regression.py  # Model implementation
├── utils/
│   ├── data_loader.py     # Data loading utilities
│   └── evaluation.py      # Model evaluation functions
└── output/
    ├── predictions.csv    # Model predictions
    └── metrics.txt        # Performance metrics
```

## Research Question
**How accurately can linear regression predict house prices based on features like area, number of rooms, and location?**

## Dataset
- **Source**: Boston Housing Dataset (from Scikit-learn)
- **Features**: 13 features including area, rooms, location factors
- **Target**: Median value of homes (in $1000s)

## Features Used
1. **CRIM**: Per capita crime rate
2. **ZN**: Proportion of residential land
3. **INDUS**: Proportion of non-retail business acres
4. **CHAS**: Charles River dummy variable
5. **NOX**: Nitric oxides concentration
6. **RM**: Average number of rooms per dwelling
7. **AGE**: Proportion of owner-occupied units built prior to 1940
8. **DIS**: Weighted distances to employment centers
9. **RAD**: Index of accessibility to radial highways
10. **TAX**: Property tax rate
11. **PTRATIO**: Pupil-teacher ratio
12. **B**: Proportion of Black residents
13. **LSTAT**: Lower status of population

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

## Evaluation Metrics
- **R² Score**: Coefficient of determination
- **Mean Absolute Error (MAE)**
- **Mean Squared Error (MSE)**
- **Root Mean Squared Error (RMSE)**

## Expected Output
- Model predictions saved to `output/predictions.csv`
- Performance metrics saved to `output/metrics.txt`
- Visualization plots for actual vs predicted values

## Author
Advanced Data Analytics Lab Project
