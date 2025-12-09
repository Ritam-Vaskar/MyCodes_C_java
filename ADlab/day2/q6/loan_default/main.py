"""Loan Default Analysis - Main Script"""
import os, sys
import pandas as pd
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from model.linear_regression import LoanDefaultPredictor
from utils.data_loader import load_loan_default_data, preprocess_loan_data, prepare_features_target
from utils.evaluation import evaluate_model, plot_predictions, plot_residuals, plot_feature_importance, plot_correlation_matrix, save_metrics_to_file

def main():
    print("\n" + "="*80)
    print(" LOAN DEFAULT ANALYSIS ".center(80))
    print("="*80)
    print("\nResearch: How do income, credit score, loan amount, and loan term")
    print("affect loan default likelihood?")
    print("="*80 + "\n")
    
    os.makedirs("output/visualizations", exist_ok=True)
    
    df = load_loan_default_data()
    df_processed = preprocess_loan_data(df)
    X, y = prepare_features_target(df_processed)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"\n[+] Train: {len(X_train)} | Test: {len(X_test)}")
    
    predictor = LoanDefaultPredictor(normalize=True)
    predictor.train(X_train, y_train)
    
    y_pred = predictor.predict(X_test)
    metrics = evaluate_model(y_test, y_pred)
    
    coefficients_df = predictor.get_coefficients()
    print(f"\n[+] Top 15 Features:")
    print(coefficients_df.head(15).to_string(index=False))
    
    print("\n[+] Generating visualizations...")
    plot_predictions(y_test, y_pred, "Loan Default Rate: Actual vs Predicted", "output/visualizations/predictions.png")
    plot_residuals(y_test, y_pred, "output/visualizations/residuals.png")
    plot_feature_importance(coefficients_df, 15, "output/visualizations/features.png")
    plot_correlation_matrix(df_processed, save_path="output/visualizations/correlation.png")
    
    pd.DataFrame({'Actual': y_test.values, 'Predicted': y_pred}).to_csv("output/predictions.csv", index=False)
    coefficients_df.to_csv("output/coefficients.csv", index=False)
    save_metrics_to_file(metrics, "output/metrics.txt")
    
    print(f"\n{'='*80}")
    print(f" COMPLETE ".center(80))
    print(f"{'='*80}")
    print(f"R²: {metrics['R2_Score']:.4f} | MAE: {metrics['MAE']:.2f} | RMSE: {metrics['RMSE']:.2f}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
