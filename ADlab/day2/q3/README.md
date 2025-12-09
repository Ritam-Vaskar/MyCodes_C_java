# Time Series Forecasting Using Linear Regression

## Overview
This project analyzes whether linear regression can accurately model trends in time series data by predicting temperature patterns.

## Project Structure
```
q3/
├── main.py                 # Main execution script
├── README.md              # This file
├── requirements.txt       # Dependencies
├── model/
│   └── linear_regression.py  # Time series model implementation
├── utils/
│   ├── data_loader.py     # Data loading utilities
│   └── evaluation.py      # Model evaluation functions
└── output/
    ├── predictions.csv    # Model predictions
    ├── metrics.txt        # Performance metrics
    ├── forecast.csv       # Future forecasts
    └── visualizations/    # Plots and charts
```

## Research Question
**Can linear regression accurately model trends in time series data, such as predicting temperature or stock prices?**

## Dataset
- **Source**: Weather Dataset (online)
- **Features**: 
  - Date/Time
  - Historical temperature data
  - Seasonal patterns
- **Target**: Temperature (in degrees)

## Time Series Components
1. **Trend**: Long-term increase or decrease
2. **Seasonality**: Periodic patterns
3. **Residuals**: Random variations

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
- **Trend Analysis**: Linear trend detection

## Expected Output
- Model predictions and performance metrics
- Time series visualization with trend line
- Forecast for future time periods
- Residual analysis
- Seasonal decomposition

## Author
Advanced Data Analytics Lab Project
