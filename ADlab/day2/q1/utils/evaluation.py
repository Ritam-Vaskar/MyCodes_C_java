"""
Model Evaluation Utilities
"""

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns


def evaluate_model(y_true, y_pred, model_name="Linear Regression"):
    """
    Evaluate model performance using multiple metrics
    """
    # Calculate metrics
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    
    # Calculate percentage errors
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    print("\n" + "="*60)
    print(f"{model_name} - PERFORMANCE METRICS")
    print("="*60)
    print(f"R² Score:                    {r2:.4f}")
    print(f"Mean Absolute Error (MAE):   ${mae:.2f}k")
    print(f"Mean Squared Error (MSE):    {mse:.2f}")
    print(f"Root Mean Squared Error:     ${rmse:.2f}k")
    print(f"Mean Absolute % Error:       {mape:.2f}%")
    print("="*60)
    
    # Interpretation
    print("\nModel Performance Interpretation:")
    if r2 >= 0.8:
        print(f"✓ Excellent fit (R² = {r2:.4f})")
    elif r2 >= 0.6:
        print(f"✓ Good fit (R² = {r2:.4f})")
    elif r2 >= 0.4:
        print(f"⚠ Moderate fit (R² = {r2:.4f})")
    else:
        print(f"✗ Poor fit (R² = {r2:.4f})")
    
    print(f"On average, predictions are off by ${mae:.2f}k ({mape:.2f}%)")
    
    metrics = {
        'R2_Score': r2,
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'MAPE': mape
    }
    
    return metrics


def plot_predictions(y_true, y_pred, save_path=None):
    """
    Plot actual vs predicted values
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Scatter plot: Actual vs Predicted
    axes[0].scatter(y_true, y_pred, alpha=0.6, edgecolors='k', linewidth=0.5)
    axes[0].plot([y_true.min(), y_true.max()], 
                 [y_true.min(), y_true.max()], 
                 'r--', lw=2, label='Perfect Prediction')
    axes[0].set_xlabel('Actual Price ($1000s)', fontsize=12)
    axes[0].set_ylabel('Predicted Price ($1000s)', fontsize=12)
    axes[0].set_title('Actual vs Predicted House Prices', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Residual plot
    residuals = y_true - y_pred
    axes[1].scatter(y_pred, residuals, alpha=0.6, edgecolors='k', linewidth=0.5)
    axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
    axes[1].set_xlabel('Predicted Price ($1000s)', fontsize=12)
    axes[1].set_ylabel('Residuals', fontsize=12)
    axes[1].set_title('Residual Plot', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nPlot saved to: {save_path}")
    
    plt.show()


def plot_feature_importance(model, feature_names, save_path=None):
    """
    Plot feature importance (coefficients)
    """
    importance = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': model.coef_
    }).sort_values('Coefficient', key=abs, ascending=False)
    
    plt.figure(figsize=(10, 6))
    colors = ['green' if x > 0 else 'red' for x in importance['Coefficient']]
    plt.barh(importance['Feature'], importance['Coefficient'], color=colors, alpha=0.7)
    plt.xlabel('Coefficient Value', fontsize=12)
    plt.ylabel('Features', fontsize=12)
    plt.title('Feature Importance (Linear Regression Coefficients)', 
              fontsize=14, fontweight='bold')
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
        f.write("LINEAR REGRESSION MODEL - PERFORMANCE METRICS\n")
        f.write("Boston Housing Dataset\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"R2 Score:                    {metrics['R2_Score']:.4f}\n")
        f.write(f"Mean Absolute Error (MAE):   ${metrics['MAE']:.2f}k\n")
        f.write(f"Mean Squared Error (MSE):    {metrics['MSE']:.2f}\n")
        f.write(f"Root Mean Squared Error:     ${metrics['RMSE']:.2f}k\n")
        f.write(f"Mean Absolute % Error:       {metrics['MAPE']:.2f}%\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("INTERPRETATION\n")
        f.write("="*60 + "\n")
        
        if metrics['R2_Score'] >= 0.8:
            f.write(f"[+] Excellent model fit (R2 = {metrics['R2_Score']:.4f})\n")
        elif metrics['R2_Score'] >= 0.6:
            f.write(f"[+] Good model fit (R2 = {metrics['R2_Score']:.4f})\n")
        else:
            f.write(f"[!] Moderate model fit (R2 = {metrics['R2_Score']:.4f})\n")
        
        f.write(f"\nOn average, predictions are off by ${metrics['MAE']:.2f}k\n")
        f.write(f"This represents a {metrics['MAPE']:.2f}% error rate.\n")
    
    print(f"\nMetrics saved to: {filepath}")


import pandas as pd
