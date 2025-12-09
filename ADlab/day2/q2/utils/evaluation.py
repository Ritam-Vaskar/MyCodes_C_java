"""
Model Evaluation Utilities
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns


def evaluate_model(y_true, y_pred, model_name="Linear Regression"):
    """
    Evaluate model performance using multiple metrics
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
    print(f"Mean Absolute Error (MAE):   {mae:.2f}k units")
    print(f"Mean Squared Error (MSE):    {mse:.2f}")
    print(f"Root Mean Squared Error:     {rmse:.2f}k units")
    print(f"Mean Absolute % Error:       {mape:.2f}%")
    print("="*60)
    
    print("\nModel Performance Interpretation:")
    if r2 >= 0.8:
        print(f"[+] Excellent fit (R2 = {r2:.4f})")
        print("    Linear regression strongly explains the relationship")
    elif r2 >= 0.6:
        print(f"[+] Good fit (R2 = {r2:.4f})")
        print("    Linear regression well explains the relationship")
    elif r2 >= 0.4:
        print(f"[!] Moderate fit (R2 = {r2:.4f})")
        print("    Linear regression moderately explains the relationship")
    else:
        print(f"[-] Poor fit (R2 = {r2:.4f})")
        print("    Linear regression poorly explains the relationship")
    
    print(f"\nOn average, predictions are off by {mae:.2f}k units ({mape:.2f}%)")
    
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
    
    # Scatter plot
    axes[0].scatter(y_true, y_pred, alpha=0.6, edgecolors='k', linewidth=0.5)
    axes[0].plot([y_true.min(), y_true.max()], 
                 [y_true.min(), y_true.max()], 
                 'r--', lw=2, label='Perfect Prediction')
    axes[0].set_xlabel('Actual Sales (thousands)', fontsize=12)
    axes[0].set_ylabel('Predicted Sales (thousands)', fontsize=12)
    axes[0].set_title('Actual vs Predicted Sales', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Residual plot
    residuals = y_true - y_pred
    axes[1].scatter(y_pred, residuals, alpha=0.6, edgecolors='k', linewidth=0.5)
    axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
    axes[1].set_xlabel('Predicted Sales (thousands)', fontsize=12)
    axes[1].set_ylabel('Residuals', fontsize=12)
    axes[1].set_title('Residual Plot', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nPrediction plot saved to: {save_path}")
    
    plt.show()


def plot_correlation_heatmap(X, y, save_path=None):
    """
    Plot correlation heatmap
    """
    data = X.copy()
    data['Sales'] = y
    
    plt.figure(figsize=(8, 6))
    corr_matrix = data.corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', 
                center=0, square=True, linewidths=1)
    plt.title('Correlation Matrix: Advertising Channels and Sales', 
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Correlation heatmap saved to: {save_path}")
    
    plt.show()


def plot_channel_analysis(X, y, save_path=None):
    """
    Plot individual channel impact on sales
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    channels = ['TV', 'Radio', 'Newspaper']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for idx, (channel, color) in enumerate(zip(channels, colors)):
        axes[idx].scatter(X[channel], y, alpha=0.6, color=color, edgecolors='k', linewidth=0.5)
        
        # Add trend line
        z = np.polyfit(X[channel], y, 1)
        p = np.poly1d(z)
        axes[idx].plot(X[channel], p(X[channel]), "r--", lw=2, alpha=0.8)
        
        axes[idx].set_xlabel(f'{channel} Budget ($1000s)', fontsize=11)
        axes[idx].set_ylabel('Sales (thousands)', fontsize=11)
        axes[idx].set_title(f'{channel} vs Sales', fontsize=12, fontweight='bold')
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Channel analysis plot saved to: {save_path}")
    
    plt.show()


def plot_feature_importance(model, feature_names, save_path=None):
    """
    Plot feature importance (coefficients)
    """
    importance = pd.DataFrame({
        'Channel': feature_names,
        'Coefficient': model.coef_,
        'Impact': ['$' + f"{abs(c):.4f}" for c in model.coef_]
    }).sort_values('Coefficient', key=abs, ascending=False)
    
    plt.figure(figsize=(10, 5))
    colors = ['green' if x > 0 else 'red' for x in importance['Coefficient']]
    bars = plt.barh(importance['Channel'], importance['Coefficient'], color=colors, alpha=0.7)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, importance['Coefficient'])):
        plt.text(val, bar.get_y() + bar.get_height()/2, 
                f' {val:.4f}', va='center', fontsize=10)
    
    plt.xlabel('Coefficient Value (Sales per $1000 spent)', fontsize=12)
    plt.ylabel('Advertising Channel', fontsize=12)
    plt.title('Advertising Channel Impact on Sales', fontsize=14, fontweight='bold')
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
        f.write("Advertising Dataset - Sales Prediction\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"R2 Score:                    {metrics['R2_Score']:.4f}\n")
        f.write(f"Mean Absolute Error (MAE):   {metrics['MAE']:.2f}k units\n")
        f.write(f"Mean Squared Error (MSE):    {metrics['MSE']:.2f}\n")
        f.write(f"Root Mean Squared Error:     {metrics['RMSE']:.2f}k units\n")
        f.write(f"Mean Absolute % Error:       {metrics['MAPE']:.2f}%\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("INTERPRETATION\n")
        f.write("="*60 + "\n")
        
        if metrics['R2_Score'] >= 0.8:
            f.write(f"[+] Excellent model fit (R2 = {metrics['R2_Score']:.4f})\n")
            f.write("Linear regression strongly explains the relationship\n")
        elif metrics['R2_Score'] >= 0.6:
            f.write(f"[+] Good model fit (R2 = {metrics['R2_Score']:.4f})\n")
            f.write("Linear regression well explains the relationship\n")
        else:
            f.write(f"[!] Moderate model fit (R2 = {metrics['R2_Score']:.4f})\n")
            f.write("Linear regression moderately explains the relationship\n")
        
        f.write(f"\nOn average, predictions are off by {metrics['MAE']:.2f}k units\n")
        f.write(f"This represents a {metrics['MAPE']:.2f}% error rate.\n")
    
    print(f"\nMetrics saved to: {filepath}")
