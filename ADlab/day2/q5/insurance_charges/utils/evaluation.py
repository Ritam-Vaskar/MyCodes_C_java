"""
Evaluation utilities for Student Performance Prediction
"""
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import os

def evaluate_model(y_true, y_pred, model_name="Linear Regression"):
    """
    Evaluate model performance using multiple metrics
    
    Args:
        y_true (array-like): True values
        y_pred (array-like): Predicted values
        model_name (str): Name of the model
        
    Returns:
        dict: Dictionary of evaluation metrics
    """
    print(f"\n{'='*60}")
    print(f"Model Performance: {model_name}")
    print(f"{'='*60}")
    
    # Calculate metrics
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    
    # Calculate MAPE (avoiding division by zero)
    mask = y_true != 0
    if mask.sum() > 0:
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    else:
        mape = np.nan
    
    # Calculate percentage within tolerance
    tolerance_1 = np.mean(np.abs(y_true - y_pred) <= 1) * 100
    tolerance_2 = np.mean(np.abs(y_true - y_pred) <= 2) * 100
    
    metrics = {
        'R2_Score': r2,
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'MAPE': mape,
        'Within_1_Point': tolerance_1,
        'Within_2_Points': tolerance_2
    }
    
    # Print metrics
    print(f"R-squared (R2) Score    : {r2:.4f}")
    print(f"Mean Absolute Error     : {mae:.4f} points")
    print(f"Mean Squared Error      : {mse:.4f}")
    print(f"Root Mean Squared Error : {rmse:.4f} points")
    if not np.isnan(mape):
        print(f"Mean Absolute % Error   : {mape:.2f}%")
    print(f"Predictions within 1 pt : {tolerance_1:.2f}%")
    print(f"Predictions within 2 pts: {tolerance_2:.2f}%")
    print(f"{'='*60}\n")
    
    return metrics

def plot_predictions(y_true, y_pred, title="Actual vs Predicted Grades", save_path=None):
    """
    Plot actual vs predicted values
    
    Args:
        y_true (array-like): True values
        y_pred (array-like): Predicted values
        title (str): Plot title
        save_path (str): Path to save the plot
    """
    plt.figure(figsize=(10, 6))
    
    # Scatter plot
    plt.scatter(y_true, y_pred, alpha=0.6, edgecolors='k', linewidth=0.5)
    
    # Perfect prediction line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
    
    plt.xlabel('Actual Grade', fontsize=12)
    plt.ylabel('Predicted Grade', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[+] Plot saved: {save_path}")
    
    plt.close()

def plot_residuals(y_true, y_pred, save_path=None):
    """
    Plot residuals distribution
    
    Args:
        y_true (array-like): True values
        y_pred (array-like): Predicted values
        save_path (str): Path to save the plot
    """
    residuals = y_true - y_pred
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Residual plot
    axes[0].scatter(y_pred, residuals, alpha=0.6, edgecolors='k', linewidth=0.5)
    axes[0].axhline(y=0, color='r', linestyle='--', linewidth=2)
    axes[0].set_xlabel('Predicted Grade', fontsize=12)
    axes[0].set_ylabel('Residuals', fontsize=12)
    axes[0].set_title('Residual Plot', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # Residual distribution
    axes[1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
    axes[1].axvline(x=0, color='r', linestyle='--', linewidth=2)
    axes[1].set_xlabel('Residuals', fontsize=12)
    axes[1].set_ylabel('Frequency', fontsize=12)
    axes[1].set_title('Residual Distribution', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[+] Plot saved: {save_path}")
    
    plt.close()

def plot_feature_importance(coefficients_df, top_n=15, save_path=None):
    """
    Plot feature importance based on coefficients
    
    Args:
        coefficients_df (pd.DataFrame): DataFrame with features and coefficients
        top_n (int): Number of top features to display
        save_path (str): Path to save the plot
    """
    # Get top N features
    top_features = coefficients_df.head(top_n)
    
    plt.figure(figsize=(12, 8))
    
    # Create horizontal bar plot
    colors = ['green' if x > 0 else 'red' for x in top_features['Coefficient']]
    plt.barh(range(len(top_features)), top_features['Coefficient'], color=colors, alpha=0.7, edgecolor='black')
    plt.yticks(range(len(top_features)), top_features['Feature'])
    plt.xlabel('Coefficient Value', fontsize=12)
    plt.ylabel('Features', fontsize=12)
    plt.title(f'Top {top_n} Most Influential Features', fontsize=14, fontweight='bold')
    plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[+] Plot saved: {save_path}")
    
    plt.close()

def plot_feature_group_importance(group_df, save_path=None):
    """
    Plot importance of feature groups
    
    Args:
        group_df (pd.DataFrame): DataFrame with feature group importance
        save_path (str): Path to save the plot
    """
    plt.figure(figsize=(10, 6))
    
    plt.bar(range(len(group_df)), group_df['Total_Abs_Coefficient'], 
            alpha=0.7, edgecolor='black', color='steelblue')
    plt.xticks(range(len(group_df)), group_df['Feature_Group'], rotation=45, ha='right')
    plt.xlabel('Feature Group', fontsize=12)
    plt.ylabel('Total Absolute Coefficient', fontsize=12)
    plt.title('Feature Group Importance Analysis', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[+] Plot saved: {save_path}")
    
    plt.close()

def plot_correlation_matrix(df, features_to_include=None, save_path=None):
    """
    Plot correlation matrix heatmap
    
    Args:
        df (pd.DataFrame): Dataset
        features_to_include (list): List of features to include
        save_path (str): Path to save the plot
    """
    if features_to_include:
        df_subset = df[features_to_include]
    else:
        # Select only numeric columns
        df_subset = df.select_dtypes(include=[np.number])
    
    # Calculate correlation matrix
    corr_matrix = df_subset.corr()
    
    # Create plot
    plt.figure(figsize=(14, 12))
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[+] Plot saved: {save_path}")
    
    plt.close()

def plot_grade_distribution(y_train, y_test, y_pred, save_path=None):
    """
    Plot distribution of actual and predicted grades
    
    Args:
        y_train (array-like): Training grades
        y_test (array-like): Test grades
        y_pred (array-like): Predicted grades
        save_path (str): Path to save the plot
    """
    plt.figure(figsize=(12, 6))
    
    plt.hist(y_train, bins=20, alpha=0.5, label='Training Grades', edgecolor='black')
    plt.hist(y_test, bins=20, alpha=0.5, label='Test Actual Grades', edgecolor='black')
    plt.hist(y_pred, bins=20, alpha=0.5, label='Test Predicted Grades', edgecolor='black')
    
    plt.xlabel('Grade', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Grade Distribution Comparison', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[+] Plot saved: {save_path}")
    
    plt.close()

def save_metrics_to_file(metrics, file_path):
    """
    Save evaluation metrics to text file
    
    Args:
        metrics (dict): Dictionary of metrics
        file_path (str): Path to save the file
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("Student Performance Prediction - Evaluation Metrics\n")
        f.write("="*60 + "\n\n")
        
        for metric_name, metric_value in metrics.items():
            if not np.isnan(metric_value):
                if 'Within' in metric_name or 'MAPE' in metric_name:
                    f.write(f"{metric_name.replace('_', ' '):<30}: {metric_value:.2f}%\n")
                else:
                    f.write(f"{metric_name.replace('_', ' '):<30}: {metric_value:.4f}\n")
        
        f.write("\n" + "="*60 + "\n")
    
    print(f"[+] Metrics saved: {file_path}")
