"""
Main Script: Car Mileage Prediction using Linear Regression
Research Question: What is the impact of engine size, weight, horsepower, 
and fuel type on car mileage?
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.linear_regression import MPGPredictor
from utils.data_loader import load_auto_mpg_data, preprocess_auto_mpg, prepare_features_target
from utils.evaluation import evaluate_model, plot_predictions, plot_residuals, plot_feature_importance, plot_correlation_matrix, save_metrics_to_file

def main():
    print("\n" + "="*80)
    print(" CAR MILEAGE PREDICTION USING LINEAR REGRESSION ".center(80))
    print("="*80)
    print("\nResearch Question:")
    print("What is the impact of engine size, weight, horsepower, and fuel type on car mileage?")
    print("="*80 + "\n")
    
    output_dir = "output"
    viz_dir = os.path.join(output_dir, "visualizations")
    os.makedirs(viz_dir, exist_ok=True)
    
    # Load and preprocess data
    df = load_auto_mpg_data()
    df_processed = preprocess_auto_mpg(df)
    X, y = prepare_features_target(df_processed, target_col='mpg')
    
    # Split data
    print("\n[+] Splitting data (80-20)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"[+] Training: {len(X_train)} cars | Test: {len(X_test)} cars")
    
    # Train model
    predictor = MPGPredictor(normalize=True)
    predictor.train(X_train, y_train)
    
    # Make predictions
    print("\n[+] Making predictions...")
    y_pred = predictor.predict(X_test)
    
    # Evaluate
    metrics = evaluate_model(y_test, y_pred)
    
    # Analyze features
    print("\n[+] Top 10 Most Influential Features:")
    coefficients_df = predictor.get_coefficients()
    print(coefficients_df.head(10).to_string(index=False))
    
    # Generate visualizations
    print("\n[+] Generating visualizations...")
    plot_predictions(y_test, y_pred, save_path=os.path.join(viz_dir, "predictions.png"))
    plot_residuals(y_test, y_pred, save_path=os.path.join(viz_dir, "residuals.png"))
    plot_feature_importance(coefficients_df, save_path=os.path.join(viz_dir, "feature_importance.png"))
    plot_correlation_matrix(df_processed, save_path=os.path.join(viz_dir, "correlation.png"))
    
    # Save results
    print("\n[+] Saving results...")
    predictions_df = pd.DataFrame({'Actual_MPG': y_test.values, 'Predicted_MPG': y_pred, 'Error': y_test.values - y_pred})
    predictions_df.to_csv(os.path.join(output_dir, "predictions.csv"), index=False)
    coefficients_df.to_csv(os.path.join(output_dir, "coefficients.csv"), index=False)
    save_metrics_to_file(metrics, os.path.join(output_dir, "metrics.txt"))
    
    print("\n" + "="*80)
    print(" ANALYSIS COMPLETE ".center(80))
    print("="*80)
    print(f"\nR² Score: {metrics['R2_Score']:.4f}")
    print(f"MAE: {metrics['MAE']:.4f} MPG")
    print(f"RMSE: {metrics['RMSE']:.4f} MPG")
    print(f"\nResults saved to: {output_dir}/")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
