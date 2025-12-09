"""
Main Script: Time Series Forecasting Using Linear Regression
Temperature Prediction Analysis
"""

import sys
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_loader import (load_data, prepare_time_series_features, 
                               split_time_series_data, get_data_statistics,
                               detect_trend, analyze_seasonality)
from utils.evaluation import (evaluate_model, plot_time_series_predictions,
                              plot_forecast_with_trend, plot_seasonal_decomposition,
                              plot_feature_importance, save_metrics_to_file)
from model.linear_regression import TimeSeriesPredictor


def main():
    """
    Main execution function
    """
    print("\n" + "="*70)
    print("TIME SERIES FORECASTING USING LINEAR REGRESSION")
    print("="*70)
    print("\nResearch Question:")
    print("Can linear regression accurately model trends in time series data,")
    print("such as predicting temperature or stock prices?")
    print("\nDataset: Weather Dataset (Temperature Time Series)")
    print("="*70)
    
    # Step 1: Load Data
    print("\n[STEP 1] Loading Dataset...")
    df = load_data()
    
    # Step 2: Data Statistics
    print("\n[STEP 2] Analyzing Time Series...")
    get_data_statistics(df)
    
    # Step 3: Prepare Features
    print("\n[STEP 3] Preparing Time Series Features...")
    df = prepare_time_series_features(df)
    
    # Step 4: Trend and Seasonality Analysis
    print("\n[STEP 4] Analyzing Trends and Patterns...")
    slope, intercept, r_value = detect_trend(df)
    monthly_patterns = analyze_seasonality(df)
    
    # Step 5: Split Data (chronological)
    print("\n[STEP 5] Splitting Time Series...")
    train_df, test_df = split_time_series_data(df, test_size=0.2)
    
    # Prepare features and target
    feature_cols = ['TimeIndex', 'Sin_DayOfYear', 'Cos_DayOfYear', 
                    'Month', 'DayOfWeek']
    
    X_train = train_df[feature_cols].values
    y_train = train_df['Temperature'].values
    X_test = test_df[feature_cols].values
    y_test = test_df['Temperature'].values
    
    # Step 6: Train Model
    print("\n[STEP 6] Training Time Series Model...")
    predictor = TimeSeriesPredictor(normalize=True)
    predictor.train(X_train, y_train, feature_cols)
    predictor.set_last_time_index(train_df['TimeIndex'].max())
    
    # Display equation
    predictor.print_equation()
    
    # Analyze components
    components = predictor.analyze_components()
    
    # Step 7: Make Predictions
    print("\n[STEP 7] Making Predictions...")
    y_pred_train = predictor.predict(X_train)
    y_pred_test = predictor.predict(X_test)
    
    print(f"[+] Predictions generated for {len(y_pred_test)} test samples")
    
    # Step 8: Evaluate Model
    print("\n[STEP 8] Evaluating Model Performance...")
    
    print("\n--- Training Set Performance ---")
    train_metrics = evaluate_model(y_train, y_pred_train, "Training Set")
    
    print("\n--- Testing Set Performance ---")
    test_metrics = evaluate_model(y_test, y_pred_test, "Testing Set")
    
    # Step 9: Future Forecast
    print("\n[STEP 9] Generating Future Forecast...")
    last_date = df['Date'].max()
    forecast_df = predictor.forecast_future(last_date, n_days=30)
    
    print(f"[+] 30-day forecast generated")
    print(f"Forecast period: {forecast_df['Date'].min()} to {forecast_df['Date'].max()}")
    print(f"\nForecast summary:")
    print(f"  Mean predicted temperature: {forecast_df['Predicted_Temperature'].mean():.2f}°")
    print(f"  Min predicted temperature: {forecast_df['Predicted_Temperature'].min():.2f}°")
    print(f"  Max predicted temperature: {forecast_df['Predicted_Temperature'].max():.2f}°")
    
    # Step 10: Save Results
    print("\n[STEP 10] Saving Results...")
    
    # Create output directories
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    viz_dir = os.path.join(output_dir, 'visualizations')
    os.makedirs(viz_dir, exist_ok=True)
    
    # Save predictions
    test_results = test_df[['Date', 'Temperature']].copy()
    test_results['Predicted_Temperature'] = y_pred_test
    test_results['Difference'] = test_results['Temperature'] - y_pred_test
    test_results['Percentage_Error'] = np.abs(test_results['Difference'] / test_results['Temperature']) * 100
    
    predictions_path = os.path.join(output_dir, 'predictions.csv')
    test_results.to_csv(predictions_path, index=False)
    print(f"[+] Predictions saved to: {predictions_path}")
    
    # Save metrics
    metrics_path = os.path.join(output_dir, 'metrics.txt')
    save_metrics_to_file(test_metrics, metrics_path)
    
    # Save forecast
    forecast_path = os.path.join(output_dir, 'forecast.csv')
    forecast_df[['Date', 'Predicted_Temperature']].to_csv(forecast_path, index=False)
    print(f"[+] Forecast saved to: {forecast_path}")
    
    # Save coefficients
    coef_path = os.path.join(output_dir, 'coefficients.csv')
    components.to_csv(coef_path, index=False)
    print(f"[+] Coefficients saved to: {coef_path}")
    
    # Step 11: Visualizations
    print("\n[STEP 11] Generating Visualizations...")
    
    ts_plot_path = os.path.join(viz_dir, 'time_series_predictions.png')
    plot_time_series_predictions(test_df['Date'], y_test, y_pred_test, save_path=ts_plot_path)
    
    forecast_plot_path = os.path.join(viz_dir, 'forecast_with_trend.png')
    plot_forecast_with_trend(train_df, test_df, y_pred_test, save_path=forecast_plot_path)
    
    seasonal_path = os.path.join(viz_dir, 'seasonal_analysis.png')
    plot_seasonal_decomposition(df, save_path=seasonal_path)
    
    importance_path = os.path.join(viz_dir, 'feature_importance.png')
    plot_feature_importance(predictor.model, feature_cols, save_path=importance_path)
    
    # Final Summary
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print(f"\n[+] Linear Regression achieved R2 = {test_metrics['R2_Score']:.4f}")
    print(f"[+] Average prediction error: {test_metrics['MAE']:.2f}° ({test_metrics['MAPE']:.2f}%)")
    
    r2 = test_metrics['R2_Score']
    if r2 >= 0.7:
        accuracy = "ACCURATELY"
        detail = f"The model explains {r2*100:.1f}% of temperature variations."
    elif r2 >= 0.5:
        accuracy = "MODERATELY WELL"
        detail = f"The model explains {r2*100:.1f}% of temperature variations."
    else:
        accuracy = "POORLY"
        detail = f"The model only explains {r2*100:.1f}% of temperature variations."
    
    print(f"\n[+] Linear regression {accuracy} models time series trends.")
    print(f"    {detail}")
    
    # Trend insight
    if abs(slope) > 0.001:
        trend_direction = "increasing" if slope > 0 else "decreasing"
        print(f"\n[+] Detected {trend_direction} temperature trend:")
        print(f"    {abs(slope*365):.4f}° change per year")
    
    print("\n[+] 30-day forecast generated with mean temperature:")
    print(f"    {forecast_df['Predicted_Temperature'].mean():.2f}°")
    
    print("\n[+] All results saved to 'output/' directory")
    print("="*70)
    
    return predictor, test_metrics


if __name__ == "__main__":
    try:
        predictor, metrics = main()
        print("\n[+] Program completed successfully!")
    except Exception as e:
        print(f"\n[-] Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
