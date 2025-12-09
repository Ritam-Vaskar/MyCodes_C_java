"""
Main Script: Student Performance Analysis using Linear Regression
Research Question: How do factors such as study hours, attendance, socioeconomic 
background, and parental education impact academic performance?
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.linear_regression import StudentPerformancePredictor
from utils.data_loader import (
    load_student_data, 
    preprocess_student_data,
    prepare_features_target,
    get_feature_groups
)
from utils.evaluation import (
    evaluate_model,
    plot_predictions,
    plot_residuals,
    plot_feature_importance,
    plot_feature_group_importance,
    plot_correlation_matrix,
    plot_grade_distribution,
    save_metrics_to_file
)

def main():
    """
    Main execution pipeline for student performance analysis
    """
    print("\n" + "="*80)
    print(" STUDENT PERFORMANCE ANALYSIS USING LINEAR REGRESSION ".center(80))
    print("="*80)
    print("\nResearch Question:")
    print("How do factors such as study hours, attendance, socioeconomic background,")
    print("and parental education impact academic performance?")
    print("="*80 + "\n")
    
    # Create output directories
    output_dir = "output"
    viz_dir = os.path.join(output_dir, "visualizations")
    os.makedirs(viz_dir, exist_ok=True)
    
    # ========================================
    # STEP 1: Load Dataset
    # ========================================
    print("\n[STEP 1] Loading Student Performance Dataset...")
    df = load_student_data()
    
    # Display basic statistics
    print(f"\n[+] Dataset Overview:")
    print(f"    [-] Total students: {len(df)}")
    print(f"    [-] Total features: {len(df.columns)}")
    print(f"    [-] Target variable: G3 (Final Grade)")
    
    if 'G3' in df.columns:
        print(f"    [-] Grade range: {df['G3'].min():.1f} - {df['G3'].max():.1f}")
        print(f"    [-] Average grade: {df['G3'].mean():.2f}")
        print(f"    [-] Std deviation: {df['G3'].std():.2f}")
    
    # ========================================
    # STEP 2: Preprocess Data
    # ========================================
    print("\n[STEP 2] Preprocessing Data...")
    df_processed, encoders = preprocess_student_data(df)
    
    # ========================================
    # STEP 3: Prepare Features and Target
    # ========================================
    print("\n[STEP 3] Preparing Features and Target Variable...")
    X, y = prepare_features_target(df_processed, target_col='G3')
    
    # Get feature groups for analysis
    feature_groups = get_feature_groups()
    
    # ========================================
    # STEP 4: Split Data
    # ========================================
    print("\n[STEP 4] Splitting Data into Training and Test Sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"[+] Training set: {len(X_train)} students")
    print(f"[+] Test set: {len(X_test)} students")
    print(f"[+] Split ratio: 80-20")
    
    # ========================================
    # STEP 5: Train Model
    # ========================================
    print("\n[STEP 5] Training Linear Regression Model...")
    predictor = StudentPerformancePredictor(normalize=True)
    predictor.train(X_train, y_train)
    
    # ========================================
    # STEP 6: Make Predictions
    # ========================================
    print("\n[STEP 6] Making Predictions on Test Set...")
    y_pred = predictor.predict(X_test)
    
    print(f"[+] Predictions generated for {len(y_pred)} students")
    print(f"[+] Predicted grade range: {y_pred.min():.2f} - {y_pred.max():.2f}")
    print(f"[+] Average predicted grade: {y_pred.mean():.2f}")
    
    # ========================================
    # STEP 7: Evaluate Model
    # ========================================
    print("\n[STEP 7] Evaluating Model Performance...")
    metrics = evaluate_model(y_test, y_pred, model_name="Student Performance Predictor")
    
    # ========================================
    # STEP 8: Analyze Feature Importance
    # ========================================
    print("\n[STEP 8] Analyzing Feature Importance...")
    
    # Get all coefficients
    coefficients_df = predictor.get_coefficients()
    print(f"\n[+] Top 15 Most Influential Features:")
    print(coefficients_df.head(15).to_string(index=False))
    
    # Analyze feature groups
    print(f"\n[+] Feature Group Analysis:")
    group_importance = predictor.analyze_feature_groups(feature_groups)
    print(group_importance.to_string(index=False))
    
    # ========================================
    # STEP 9: Answer Research Question
    # ========================================
    print("\n" + "="*80)
    print(" RESEARCH FINDINGS ".center(80))
    print("="*80)
    
    print("\n[+] Key Factors Impacting Academic Performance:\n")
    
    top_features = coefficients_df.head(10)
    for idx, row in top_features.iterrows():
        impact = "positive" if row['Coefficient'] > 0 else "negative"
        print(f"    {idx+1}. {row['Feature']}")
        print(f"       Impact: {impact.upper()} ({row['Coefficient']:.4f})")
    
    print(f"\n[+] Feature Group Impact Ranking:\n")
    for idx, row in group_importance.iterrows():
        print(f"    {idx+1}. {row['Feature_Group']}")
        print(f"       Total Impact: {row['Total_Abs_Coefficient']:.4f}")
        print(f"       Avg Impact per Feature: {row['Avg_Abs_Coefficient']:.4f}")
        print(f"       Number of Features: {int(row['Num_Features'])}\n")
    
    print("="*80)
    
    # ========================================
    # STEP 10: Generate Visualizations
    # ========================================
    print("\n[STEP 10] Generating Visualizations...")
    
    # Plot 1: Actual vs Predicted
    plot_predictions(
        y_test, y_pred,
        title="Student Performance: Actual vs Predicted Grades",
        save_path=os.path.join(viz_dir, "actual_vs_predicted.png")
    )
    
    # Plot 2: Residuals
    plot_residuals(
        y_test, y_pred,
        save_path=os.path.join(viz_dir, "residual_analysis.png")
    )
    
    # Plot 3: Feature Importance
    plot_feature_importance(
        coefficients_df, top_n=15,
        save_path=os.path.join(viz_dir, "feature_importance.png")
    )
    
    # Plot 4: Feature Group Importance
    plot_feature_group_importance(
        group_importance,
        save_path=os.path.join(viz_dir, "feature_group_importance.png")
    )
    
    # Plot 5: Correlation Matrix
    plot_correlation_matrix(
        df_processed,
        save_path=os.path.join(viz_dir, "correlation_matrix.png")
    )
    
    # Plot 6: Grade Distribution
    plot_grade_distribution(
        y_train, y_test, y_pred,
        save_path=os.path.join(viz_dir, "grade_distribution.png")
    )
    
    print(f"\n[+] All visualizations saved to: {viz_dir}/")
    
    # ========================================
    # STEP 11: Save Results
    # ========================================
    print("\n[STEP 11] Saving Results...")
    
    # Save predictions
    predictions_df = pd.DataFrame({
        'Actual_Grade': y_test.values,
        'Predicted_Grade': y_pred,
        'Residual': y_test.values - y_pred,
        'Absolute_Error': np.abs(y_test.values - y_pred)
    })
    predictions_path = os.path.join(output_dir, "predictions.csv")
    predictions_df.to_csv(predictions_path, index=False)
    print(f"[+] Predictions saved: {predictions_path}")
    
    # Save coefficients
    coefficients_path = os.path.join(output_dir, "feature_coefficients.csv")
    coefficients_df.to_csv(coefficients_path, index=False)
    print(f"[+] Feature coefficients saved: {coefficients_path}")
    
    # Save feature group analysis
    group_analysis_path = os.path.join(output_dir, "feature_group_analysis.csv")
    group_importance.to_csv(group_analysis_path, index=False)
    print(f"[+] Feature group analysis saved: {group_analysis_path}")
    
    # Save metrics
    metrics_path = os.path.join(output_dir, "evaluation_metrics.txt")
    save_metrics_to_file(metrics, metrics_path)
    
    # Save model summary
    summary_path = os.path.join(output_dir, "model_summary.txt")
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("STUDENT PERFORMANCE ANALYSIS - MODEL SUMMARY\n")
        f.write("="*80 + "\n\n")
        
        f.write("RESEARCH QUESTION:\n")
        f.write("How do factors such as study hours, attendance, socioeconomic background,\n")
        f.write("and parental education impact academic performance?\n\n")
        
        f.write("DATASET INFORMATION:\n")
        f.write(f"Total Students: {len(df)}\n")
        f.write(f"Total Features: {len(X.columns)}\n")
        f.write(f"Training Samples: {len(X_train)}\n")
        f.write(f"Test Samples: {len(X_test)}\n\n")
        
        f.write("MODEL CONFIGURATION:\n")
        f.write(f"Algorithm: Linear Regression\n")
        f.write(f"Feature Normalization: Yes (StandardScaler)\n")
        f.write(f"Target Variable: G3 (Final Grade)\n")
        f.write(f"Model Intercept: {predictor.get_intercept():.4f}\n\n")
        
        f.write("PERFORMANCE METRICS:\n")
        for metric_name, metric_value in metrics.items():
            if not np.isnan(metric_value):
                f.write(f"{metric_name.replace('_', ' ')}: {metric_value:.4f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("TOP 10 MOST INFLUENTIAL FEATURES:\n")
        f.write("="*80 + "\n")
        for idx, row in top_features.iterrows():
            f.write(f"{idx+1:2d}. {row['Feature']:<25} : {row['Coefficient']:>10.4f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("FEATURE GROUP ANALYSIS:\n")
        f.write("="*80 + "\n")
        for idx, row in group_importance.iterrows():
            f.write(f"\n{idx+1}. {row['Feature_Group'].upper()}\n")
            f.write(f"   Total Impact: {row['Total_Abs_Coefficient']:.4f}\n")
            f.write(f"   Avg Impact: {row['Avg_Abs_Coefficient']:.4f}\n")
            f.write(f"   Features: {int(row['Num_Features'])}\n")
        
        f.write("\n" + "="*80 + "\n")
        
    print(f"[+] Model summary saved: {summary_path}")
    
    # ========================================
    # FINAL SUMMARY
    # ========================================
    print("\n" + "="*80)
    print(" ANALYSIS COMPLETE ".center(80))
    print("="*80)
    print(f"\n[+] Model Performance Summary:")
    print(f"    R-squared Score: {metrics['R2_Score']:.4f}")
    print(f"    Mean Absolute Error: {metrics['MAE']:.4f} points")
    print(f"    Predictions within 1 point: {metrics['Within_1_Point']:.2f}%")
    print(f"    Predictions within 2 points: {metrics['Within_2_Points']:.2f}%")
    
    print(f"\n[+] All results saved to: {output_dir}/")
    print(f"    [-] Predictions: predictions.csv")
    print(f"    [-] Feature Coefficients: feature_coefficients.csv")
    print(f"    [-] Group Analysis: feature_group_analysis.csv")
    print(f"    [-] Metrics: evaluation_metrics.txt")
    print(f"    [-] Summary: model_summary.txt")
    print(f"    [-] Visualizations: visualizations/ (6 plots)")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
