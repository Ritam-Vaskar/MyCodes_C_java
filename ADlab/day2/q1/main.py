"""
Main Script: House Price Prediction using Linear Regression
Boston Housing Dataset Analysis
"""

import sys
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Add project directories to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_loader import load_data, split_data, get_data_statistics
from utils.evaluation import (evaluate_model, plot_predictions, 
                              plot_feature_importance, save_metrics_to_file)
from model.linear_regression import HousePricePredictor


def main():
    """
    Main execution function
    """
    print("\n" + "="*70)
    print("PREDICTIVE POWER OF LINEAR REGRESSION IN HOUSE PRICE ESTIMATION")
    print("="*70)
    print("\nResearch Question:")
    print("How accurately can linear regression predict house prices based on")
    print("features like area, number of rooms, and location?")
    print("\nDataset: Boston Housing Dataset (Scikit-learn)")
    print("="*70)
    
    # Step 1: Load Data
    print("\n[STEP 1] Loading Dataset...")
    X, y = load_data()
    
    # Step 2: Data Statistics
    print("\n[STEP 2] Analyzing Dataset...")
    get_data_statistics(X, y)
    
    # Step 3: Split Data
    print("\n[STEP 3] Splitting Data...")
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)
    
    # Step 4: Train Model
    print("\n[STEP 4] Training Model...")
    predictor = HousePricePredictor(normalize=True)
    predictor.train(X_train, y_train)
    
    # Display regression equation
    predictor.print_equation(X.columns)
    
    # Display top features
    predictor.get_top_features(X.columns, n=5)
    
    # Step 5: Make Predictions
    print("\n[STEP 5] Making Predictions...")
    y_pred_train = predictor.predict(X_train)
    y_pred_test = predictor.predict(X_test)
    
    print(f"✓ Predictions generated for {len(y_pred_test)} test samples")
    
    # Step 6: Evaluate Model
    print("\n[STEP 6] Evaluating Model Performance...")
    
    print("\n--- Training Set Performance ---")
    train_metrics = evaluate_model(y_train, y_pred_train, "Training Set")
    
    print("\n--- Testing Set Performance ---")
    test_metrics = evaluate_model(y_test, y_pred_test, "Testing Set")
    
    # Step 7: Save Results
    print("\n[STEP 7] Saving Results...")
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save predictions
    predictions_df = pd.DataFrame({
        'Actual_Price': y_test.values,
        'Predicted_Price': y_pred_test,
        'Difference': y_test.values - y_pred_test,
        'Percentage_Error': np.abs((y_test.values - y_pred_test) / y_test.values) * 100
    })
    predictions_path = os.path.join(output_dir, 'predictions.csv')
    predictions_df.to_csv(predictions_path, index=False)
    print(f"✓ Predictions saved to: {predictions_path}")
    
    # Save metrics
    metrics_path = os.path.join(output_dir, 'metrics.txt')
    save_metrics_to_file(test_metrics, metrics_path)
    
    # Save coefficients
    coefficients = predictor.get_coefficients(X.columns)
    coef_df = pd.DataFrame(list(coefficients.items()), 
                          columns=['Feature', 'Coefficient'])
    coef_path = os.path.join(output_dir, 'coefficients.csv')
    coef_df.to_csv(coef_path, index=False)
    print(f"✓ Coefficients saved to: {coef_path}")
    
    # Step 8: Visualizations
    print("\n[STEP 8] Generating Visualizations...")
    
    plot_path = os.path.join(output_dir, 'predictions_plot.png')
    plot_predictions(y_test, y_pred_test, save_path=plot_path)
    
    importance_path = os.path.join(output_dir, 'feature_importance.png')
    plot_feature_importance(predictor.model, X.columns, save_path=importance_path)
    
    # Final Summary
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print(f"\n✓ Linear Regression achieved R² = {test_metrics['R2_Score']:.4f}")
    print(f"✓ Average prediction error: ${test_metrics['MAE']:.2f}k ({test_metrics['MAPE']:.2f}%)")
    
    if test_metrics['R2_Score'] >= 0.7:
        print("\n✓ Linear regression demonstrates STRONG predictive power for")
        print("  house price estimation based on the given features.")
    elif test_metrics['R2_Score'] >= 0.5:
        print("\n✓ Linear regression demonstrates MODERATE predictive power for")
        print("  house price estimation based on the given features.")
    else:
        print("\n⚠ Linear regression shows LIMITED predictive power.")
        print("  Consider more advanced models or feature engineering.")
    
    print("\n✓ All results saved to 'output/' directory")
    print("="*70)
    
    return predictor, test_metrics


if __name__ == "__main__":
    try:
        predictor, metrics = main()
        print("\n✓ Program completed successfully!")
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
