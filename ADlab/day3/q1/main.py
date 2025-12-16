# Q1: Binary Classification - Spam Email Detection using Logistic Regression

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, 
                             classification_report, ConfusionMatrixDisplay)
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import load_spam_data
from model.logistic_regression_model import SpamClassifier

def main():
    print("="*70)
    print("SPAM EMAIL CLASSIFICATION USING LOGISTIC REGRESSION")
    print("="*70)
    
    # Load data
    print("\n[1] Loading Spam Email Dataset...")
    emails, labels = load_spam_data(use_real_data=True)  # Set to True for real data
    print(f"    Total emails: {len(emails)}")
    print(f"    Spam emails: {sum(labels)}")
    print(f"    Non-spam emails: {len(labels) - sum(labels)}")
    print(f"    Spam percentage: {sum(labels)/len(labels)*100:.2f}%")
    
    # Split data
    print("\n[2] Splitting dataset (80-20 train-test split)...")
    X_train, X_test, y_train, y_test = train_test_split(
        emails, labels, test_size=0.2, random_state=42, stratify=labels
    )
    print(f"    Training samples: {len(X_train)}")
    print(f"    Testing samples: {len(X_test)}")
    
    # Create and train model
    print("\n[3] Training Logistic Regression Model...")
    classifier = SpamClassifier()
    classifier.train(X_train, y_train)
    print("    ✓ Model trained successfully!")
    
    # Make predictions
    print("\n[4] Making Predictions on Test Set...")
    y_pred = classifier.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n{'='*70}")
    print(f"MODEL PERFORMANCE")
    print(f"{'='*70}")
    print(f"\n📊 ACCURACY: {accuracy*100:.2f}%")
    print(f"    ({int(accuracy*len(y_test))}/{len(y_test)} emails correctly classified)")
    
    # Confusion Matrix
    print(f"\n{'='*70}")
    print("CONFUSION MATRIX")
    print(f"{'='*70}")
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n                 Predicted")
    print(f"              Non-Spam  Spam")
    print(f"Actual Non-Spam   {cm[0][0]:4d}    {cm[0][1]:4d}")
    print(f"       Spam       {cm[1][0]:4d}    {cm[1][1]:4d}")
    
    # Classification Report
    print(f"\n{'='*70}")
    print("CLASSIFICATION REPORT")
    print(f"{'='*70}")
    print("\n" + classification_report(y_test, y_pred, 
                                       target_names=['Non-Spam', 'Spam'],
                                       digits=4))
    
    # Save visualizations
    print("\n[5] Generating Visualizations...")
    classifier.visualize_results(X_test, y_test, y_pred, cm)
    print("    ✓ Visualizations saved to output/")
    
    # Save predictions
    print("\n[6] Saving Results...")
    results_df = pd.DataFrame({
        'Email': X_test,
        'Actual': ['Spam' if y == 1 else 'Non-Spam' for y in y_test],
        'Predicted': ['Spam' if y == 1 else 'Non-Spam' for y in y_pred],
        'Correct': [a == p for a, p in zip(y_test, y_pred)]
    })
    results_df.to_csv('output/predictions.csv', index=False)
    print("    ✓ Predictions saved to output/predictions.csv")
    
    # Save metrics
    with open('output/metrics.txt', 'w') as f:
        f.write("SPAM EMAIL CLASSIFICATION - MODEL METRICS\n")
        f.write("="*70 + "\n\n")
        f.write(f"Accuracy: {accuracy*100:.2f}%\n\n")
        f.write("Confusion Matrix:\n")
        f.write(f"                 Predicted\n")
        f.write(f"              Non-Spam  Spam\n")
        f.write(f"Actual Non-Spam   {cm[0][0]:4d}    {cm[0][1]:4d}\n")
        f.write(f"       Spam       {cm[1][0]:4d}    {cm[1][1]:4d}\n\n")
        f.write("Classification Report:\n")
        f.write(classification_report(y_test, y_pred, 
                                     target_names=['Non-Spam', 'Spam'],
                                     digits=4))
    print("    ✓ Metrics saved to output/metrics.txt")
    
    print(f"\n{'='*70}")
    print("✓ SPAM CLASSIFICATION COMPLETE!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
