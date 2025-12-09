# Analyzing the Relationship Between Advertising Spend and Sales

## Overview
This project analyzes how well linear regression explains the relationship between advertising spend on TV, radio, and newspaper and product sales.

## Project Structure
```
q2/
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
    ├── metrics.txt        # Performance metrics
    ├── coefficients.csv   # Feature coefficients
    └── visualizations/    # Plots and charts
```

## Research Question
**How well does linear regression explain the relationship between advertising spend on TV, radio, and newspaper and product sales?**

## Dataset
- **Source**: Advertising Dataset (online)
- **Features**: 
  - TV: Advertising budget for TV (in thousands)
  - Radio: Advertising budget for Radio (in thousands)
  - Newspaper: Advertising budget for Newspaper (in thousands)
- **Target**: Sales (in thousands of units)

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
- **Correlation Analysis**: Between each advertising channel and sales

## Expected Output
- Model predictions and performance metrics
- Correlation matrix and heatmap
- Individual channel impact analysis
- Actual vs Predicted scatter plots
- Residual analysis

## Author
Advanced Data Analytics Lab Project
