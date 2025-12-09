"""
Main Script: Advertising Spend and Sales Analysis
Linear Regression Analysis
"""

import sys
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_loader import load_data, split_data, get_data_statistics, analyze_correlations
from utils.evaluation import (evaluate_model, plot_predictions, plot_correlation_heatmap,
                              plot_channel_analysis, plot_feature_importance, save_metrics_to_file)
from model.linear_regression import SalesPredictor


def main():
    """
    Main execution function
    """
    print("\n" + "="*70)
    print("ANALYZING THE RELATIONSHIP BETWEEN ADVERTISING SPEND AND SALES")
    print("="*70)
    print("\nResearch Question:")
    print("How well does linear regression explain the relationship between")
    print("advertising spend on TV, radio, and newspaper and product sales?")
    print("\nDataset: Advertising Dataset (online)")
    print("="*70)
    
    # Step 1: Load Data
    print("\n[STEP 1] Loading Dataset...")
    X, y = load_data()
    
    # Step 2: Data Statistics
    print("\n[STEP 2] Analyzing Dataset...")
    get_data_statistics(X, y)
    
    # Step 3: Correlation Analysis
    print("\n[STEP 3] Analyzing Correlations...")
    correlations = analyze_correlations(X, y)
    
    # Step 4: Split Data
    print("\n[STEP 4] Splitting Data...")
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)
    
    # Step 5: Train Model
    print("\n[STEP 5] Training Model...")
    predictor = SalesPredictor(normalize=True)
    predictor.train(X_train, y_train)
    
    # Display regression equation
    predictor.print_equation(X.columns)
    
    # Analyze channel impact
    impact_analysis = predictor.analyze_channel_impact(X.columns)
    
    # Step 6: Make Predictions
    print("\n[STEP 6] Making Predictions...")
    y_pred_train = predictor.predict(X_train)
    y_pred_test = predictor.predict(X_test)
    
    print(f"[+] Predictions generated for {len(y_pred_test)} test samples")
    
    # Step 7: Evaluate Model
    print("\n[STEP 7] Evaluating Model Performance...")
    
    print("\n--- Training Set Performance ---")
    train_metrics = evaluate_model(y_train, y_pred_train, "Training Set")
    
    print("\n--- Testing Set Performance ---")
    test_metrics = evaluate_model(y_test, y_pred_test, "Testing Set")
    
    # Step 8: Save Results
    print("\n[STEP 8] Saving Results...")
    
    # Create output directories
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    viz_dir = os.path.join(output_dir, 'visualizations')
    os.makedirs(viz_dir, exist_ok=True)
    
    # Save predictions
    predictions_df = pd.DataFrame({
        'Actual_Sales': y_test.values,
        'Predicted_Sales': y_pred_test,
        'Difference': y_test.values - y_pred_test,
        'Percentage_Error': np.abs((y_test.values - y_pred_test) / y_test.values) * 100
    })
    predictions_path = os.path.join(output_dir, 'predictions.csv')
    predictions_df.to_csv(predictions_path, index=False)
    print(f"[+] Predictions saved to: {predictions_path}")
    
    # Save metrics
    metrics_path = os.path.join(output_dir, 'metrics.txt')
    save_metrics_to_file(test_metrics, metrics_path)
    
    # Save coefficients
    coefficients = predictor.get_coefficients(X.columns)
    coef_df = pd.DataFrame(list(coefficients.items()), 
                          columns=['Feature', 'Coefficient'])
    coef_path = os.path.join(output_dir, 'coefficients.csv')
    coef_df.to_csv(coef_path, index=False)
    print(f"[+] Coefficients saved to: {coef_path}")
    
    # Save impact analysis
    impact_path = os.path.join(output_dir, 'channel_impact.csv')
    impact_analysis.to_csv(impact_path, index=False)
    print(f"[+] Channel impact analysis saved to: {impact_path}")
    
    # Step 9: Visualizations
    print("\n[STEP 9] Generating Visualizations...")
    
    plot_path = os.path.join(viz_dir, 'predictions_plot.png')
    plot_predictions(y_test, y_pred_test, save_path=plot_path)
    
    heatmap_path = os.path.join(viz_dir, 'correlation_heatmap.png')
    plot_correlation_heatmap(X, y, save_path=heatmap_path)
    
    channel_path = os.path.join(viz_dir, 'channel_analysis.png')
    plot_channel_analysis(X, y, save_path=channel_path)
    
    importance_path = os.path.join(viz_dir, 'feature_importance.png')
    plot_feature_importance(predictor.model, X.columns, save_path=importance_path)
    
    # Final Summary
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print(f"\n[+] Linear Regression achieved R2 = {test_metrics['R2_Score']:.4f}")
    print(f"[+] Average prediction error: {test_metrics['MAE']:.2f}k units ({test_metrics['MAPE']:.2f}%)")
    
    r2 = test_metrics['R2_Score']
    if r2 >= 0.8:
        explanation = "STRONGLY"
        detail = f"{r2*100:.1f}% of the variance in sales is explained by advertising spend."
    elif r2 >= 0.6:
        explanation = "WELL"
        detail = f"{r2*100:.1f}% of the variance in sales is explained by advertising spend."
    elif r2 >= 0.4:
        explanation = "MODERATELY"
        detail = f"{r2*100:.1f}% of the variance in sales is explained by advertising spend."
    else:
        explanation = "POORLY"
        detail = f"Only {r2*100:.1f}% of the variance in sales is explained by advertising spend."
    
    print(f"\n[+] Linear regression {explanation} explains the relationship between")
    print(f"    advertising spend and sales.")
    print(f"    {detail}")
    
    # Channel insights
    print("\n[+] Key Insights:")
    top_channel = impact_analysis.iloc[0]
    print(f"    - Most effective channel: {top_channel['Channel']}")
    print(f"    - Impact: {top_channel['Coefficient']:.4f}k units per $1k spent")
    
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
