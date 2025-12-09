"""
Model Evaluation Utilities for Time Series
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns


def evaluate_model(y_true, y_pred, model_name="Linear Regression"):
    """
    Evaluate time series model performance
    """
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    print("\n" + "="*60)
    print(f"{model_name} - PERFORMANCE METRICS")
    print("="*60)
    print(f"R2 Score:                    {r2:.4f}")
    print(f"Mean Absolute Error (MAE):   {mae:.2f}°")
    print(f"Mean Squared Error (MSE):    {mse:.2f}")
    print(f"Root Mean Squared Error:     {rmse:.2f}°")
    print(f"Mean Absolute % Error:       {mape:.2f}%")
    print("="*60)
    
    print("\nModel Performance Interpretation:")
    if r2 >= 0.8:
        print(f"[+] Excellent fit (R2 = {r2:.4f})")
        print("    Linear regression accurately models the time series")
    elif r2 >= 0.6:
        print(f"[+] Good fit (R2 = {r2:.4f})")
        print("    Linear regression well models the time series")
    elif r2 >= 0.4:
        print(f"[!] Moderate fit (R2 = {r2:.4f})")
        print("    Linear regression moderately models the time series")
    else:
        print(f"[-] Poor fit (R2 = {r2:.4f})")
        print("    Linear regression poorly models the time series")
    
    print(f"\nOn average, predictions are off by {mae:.2f}° ({mape:.2f}%)")
    
    metrics = {
        'R2_Score': r2,
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'MAPE': mape
    }
    
    return metrics


def plot_time_series_predictions(dates, y_true, y_pred, save_path=None):
    """
    Plot time series with predictions
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    
    # Time series plot
    axes[0].plot(dates, y_true, label='Actual', color='blue', alpha=0.7, linewidth=1.5)
    axes[0].plot(dates, y_pred, label='Predicted', color='red', alpha=0.7, linewidth=1.5, linestyle='--')
    axes[0].set_xlabel('Date', fontsize=12)
    axes[0].set_ylabel('Temperature (°)', fontsize=12)
    axes[0].set_title('Time Series Forecast: Actual vs Predicted', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Residual plot
    residuals = y_true - y_pred
    axes[1].scatter(dates, residuals, alpha=0.5, edgecolors='k', linewidth=0.5)
    axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
    axes[1].set_xlabel('Date', fontsize=12)
    axes[1].set_ylabel('Residuals (°)', fontsize=12)
    axes[1].set_title('Residual Plot Over Time', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nTime series plot saved to: {save_path}")
    
    plt.show()


def plot_forecast_with_trend(df_train, df_test, y_pred, save_path=None):
    """
    Plot full time series with trend line and forecast
    """
    plt.figure(figsize=(14, 6))
    
    # Plot training data
    plt.plot(df_train['Date'], df_train['Temperature'], 
             label='Training Data', color='blue', alpha=0.6, linewidth=1)
    
    # Plot test data (actual)
    plt.plot(df_test['Date'], df_test['Temperature'], 
             label='Test Data (Actual)', color='green', alpha=0.6, linewidth=1.5)
    
    # Plot predictions
    plt.plot(df_test['Date'], y_pred, 
             label='Predictions', color='red', alpha=0.8, linewidth=2, linestyle='--')
    
    # Add trend line
    all_dates = pd.concat([df_train['Date'], df_test['Date']])
    x = np.arange(len(all_dates))
    all_temps = pd.concat([df_train['Temperature'], df_test['Temperature']])
    z = np.polyfit(x, all_temps, 1)
    p = np.poly1d(z)
    plt.plot(all_dates, p(x), "k--", alpha=0.5, linewidth=2, label='Linear Trend')
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Temperature (°)', fontsize=12)
    plt.title('Time Series Forecasting with Linear Regression', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Forecast plot saved to: {save_path}")
    
    plt.show()


def plot_seasonal_decomposition(df, save_path=None):
    """
    Plot seasonal patterns
    """
    monthly_avg = df.groupby('Month')['Temperature'].mean()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Monthly averages
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    axes[0].bar(range(1, 13), monthly_avg.values, color='skyblue', edgecolor='black')
    axes[0].set_xlabel('Month', fontsize=12)
    axes[0].set_ylabel('Average Temperature (°)', fontsize=12)
    axes[0].set_title('Seasonal Pattern (Monthly Averages)', fontsize=13, fontweight='bold')
    axes[0].set_xticks(range(1, 13))
    axes[0].set_xticklabels(months, rotation=45)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Distribution
    axes[1].hist(df['Temperature'], bins=30, color='lightcoral', edgecolor='black', alpha=0.7)
    axes[1].axvline(df['Temperature'].mean(), color='red', linestyle='--', 
                    linewidth=2, label=f'Mean: {df["Temperature"].mean():.2f}°')
    axes[1].set_xlabel('Temperature (°)', fontsize=12)
    axes[1].set_ylabel('Frequency', fontsize=12)
    axes[1].set_title('Temperature Distribution', fontsize=13, fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Seasonal analysis plot saved to: {save_path}")
    
    plt.show()


def plot_feature_importance(model, feature_names, save_path=None):
    """
    Plot feature importance for time series model
    """
    importance = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': model.coef_
    }).sort_values('Coefficient', key=abs, ascending=False)
    
    plt.figure(figsize=(10, 6))
    colors = ['green' if x > 0 else 'red' for x in importance['Coefficient']]
    bars = plt.barh(importance['Feature'], importance['Coefficient'], color=colors, alpha=0.7)
    
    for i, (bar, val) in enumerate(zip(bars, importance['Coefficient'])):
        plt.text(val, bar.get_y() + bar.get_height()/2, 
                f' {val:.4f}', va='center', fontsize=9)
    
    plt.xlabel('Coefficient Value', fontsize=12)
    plt.ylabel('Features', fontsize=12)
    plt.title('Feature Importance for Time Series Prediction', fontsize=14, fontweight='bold')
    plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Feature importance plot saved to: {save_path}")
    
    plt.show()
    
    return importance


def save_metrics_to_file(metrics, filepath):
    """
    Save evaluation metrics to a text file
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("LINEAR REGRESSION MODEL - TIME SERIES FORECASTING\n")
        f.write("Temperature Prediction\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"R2 Score:                    {metrics['R2_Score']:.4f}\n")
        f.write(f"Mean Absolute Error (MAE):   {metrics['MAE']:.2f} degrees\n")
        f.write(f"Mean Squared Error (MSE):    {metrics['MSE']:.2f}\n")
        f.write(f"Root Mean Squared Error:     {metrics['RMSE']:.2f} degrees\n")
        f.write(f"Mean Absolute % Error:       {metrics['MAPE']:.2f}%\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("INTERPRETATION\n")
        f.write("="*60 + "\n")
        
        if metrics['R2_Score'] >= 0.8:
            f.write(f"[+] Excellent model fit (R2 = {metrics['R2_Score']:.4f})\n")
            f.write("Linear regression accurately models time series trends\n")
        elif metrics['R2_Score'] >= 0.6:
            f.write(f"[+] Good model fit (R2 = {metrics['R2_Score']:.4f})\n")
            f.write("Linear regression well models time series trends\n")
        else:
            f.write(f"[!] Moderate model fit (R2 = {metrics['R2_Score']:.4f})\n")
            f.write("Linear regression moderately models time series trends\n")
        
        f.write(f"\nOn average, predictions are off by {metrics['MAE']:.2f} degrees\n")
        f.write(f"This represents a {metrics['MAPE']:.2f}% error rate.\n")
    
    print(f"\nMetrics saved to: {filepath}")
