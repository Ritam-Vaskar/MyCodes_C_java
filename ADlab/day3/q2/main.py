# Q2: Decision Tree Classification - Iris Species Detection

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (accuracy_score, confusion_matrix, 
                             classification_report, ConfusionMatrixDisplay)
import matplotlib.pyplot as plt
import seaborn as sns
from model.decision_tree_model import IrisClassifier

def main():
    print("="*70)
    print("IRIS SPECIES CLASSIFICATION USING DECISION TREE")
    print("="*70)
    
    # Load Iris dataset
    print("\n[1] Loading Iris Dataset...")
    iris = load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names
    
    print(f"    Total samples: {len(X)}")
    print(f"    Features: {len(feature_names)}")
    print(f"    Feature names: {', '.join(feature_names)}")
    print(f"    Classes: {', '.join(target_names)}")
    print(f"    Class distribution:")
    for i, name in enumerate(target_names):
        print(f"      {name}: {sum(y == i)} samples")
    
    # Split data
    print("\n[2] Splitting dataset (70-30 train-test split)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    print(f"    Training samples: {len(X_train)}")
    print(f"    Testing samples: {len(X_test)}")
    
    # Create and train model
    print("\n[3] Training Decision Tree Classifier...")
    classifier = IrisClassifier(max_depth=4, random_state=42)
    classifier.train(X_train, y_train)
    print("    ✓ Model trained successfully!")
    print(f"    Tree depth: {classifier.model.get_depth()}")
    print(f"    Number of leaves: {classifier.model.get_n_leaves()}")
    
    # Make predictions
    print("\n[4] Making Predictions on Test Set...")
    y_pred = classifier.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n{'='*70}")
    print(f"MODEL PERFORMANCE")
    print(f"{'='*70}")
    print(f"\n📊 ACCURACY: {accuracy*100:.2f}%")
    print(f"    ({int(accuracy*len(y_test))}/{len(y_test)} samples correctly classified)")
    
    # Confusion Matrix
    print(f"\n{'='*70}")
    print("CONFUSION MATRIX")
    print(f"{'='*70}")
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n                    Predicted")
    print(f"              Setosa  Versicolor  Virginica")
    for i, name in enumerate(target_names):
        print(f"Actual {name:10s}   {cm[i][0]:4d}      {cm[i][1]:4d}       {cm[i][2]:4d}")
    
    # Classification Report
    print(f"\n{'='*70}")
    print("CLASSIFICATION REPORT")
    print(f"{'='*70}")
    print("\n" + classification_report(y_test, y_pred, 
                                       target_names=target_names,
                                       digits=4))
    
    # Feature Importance
    print(f"\n{'='*70}")
    print("FEATURE IMPORTANCE")
    print(f"{'='*70}")
    feature_importance = classifier.get_feature_importance()
    print()
    for feature, importance in feature_importance:
        print(f"  {feature:25s}: {importance:.4f} {'█' * int(importance * 50)}")
    
    # Save visualizations
    print(f"\n[5] Generating Visualizations...")
    classifier.visualize_results(X_test, y_test, y_pred, cm, 
                                 feature_names, target_names)
    print("    ✓ Visualizations saved to output/")
    
    # Visualize decision tree
    print("\n[6] Visualizing Decision Tree...")
    classifier.visualize_tree(feature_names, target_names)
    print("    ✓ Decision tree visualization saved to output/")
    
    # Save predictions
    print("\n[7] Saving Results...")
    results_df = pd.DataFrame(X_test, columns=feature_names)
    results_df['Actual'] = [target_names[y] for y in y_test]
    results_df['Predicted'] = [target_names[y] for y in y_pred]
    results_df['Correct'] = [a == p for a, p in zip(y_test, y_pred)]
    results_df.to_csv('output/predictions.csv', index=False)
    print("    ✓ Predictions saved to output/predictions.csv")
    
    # Save metrics
    with open('output/metrics.txt', 'w') as f:
        f.write("IRIS SPECIES CLASSIFICATION - MODEL METRICS\n")
        f.write("="*70 + "\n\n")
        f.write(f"Accuracy: {accuracy*100:.2f}%\n\n")
        f.write("Confusion Matrix:\n")
        f.write(f"                    Predicted\n")
        f.write(f"              Setosa  Versicolor  Virginica\n")
        for i, name in enumerate(target_names):
            f.write(f"Actual {name:10s}   {cm[i][0]:4d}      {cm[i][1]:4d}       {cm[i][2]:4d}\n")
        f.write("\n\nClassification Report:\n")
        f.write(classification_report(y_test, y_pred, 
                                     target_names=target_names,
                                     digits=4))
        f.write("\n\nFeature Importance:\n")
        for feature, importance in feature_importance:
            f.write(f"  {feature:25s}: {importance:.4f}\n")
    print("    ✓ Metrics saved to output/metrics.txt")
    
    print(f"\n{'='*70}")
    print("✓ IRIS CLASSIFICATION COMPLETE!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
