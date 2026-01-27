"""
Q2: SVM Classification Accuracy with PCA on Breast Cancer Dataset
Objective: Analyze how SVM accuracy changes when reducing 30 features to k principal components
Compare performance with k = {2, 5, 10, 15}
Metrics: Accuracy, Precision, Recall
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report, confusion_matrix
import seaborn as sns
import os

def evaluate_pca_svm():
    """Evaluate SVM performance with different numbers of PCA components"""
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Load Breast Cancer dataset
    print("Loading Breast Cancer Dataset...")
    data = load_breast_cancer()
    X = data.data
    y = data.target
    
    print(f"Original dataset shape: {X.shape}")
    print(f"Number of features: {X.shape[1]}")
    print(f"Number of samples: {X.shape[0]}")
    print(f"Classes: {data.target_names}")
    
    # Split the data
    print("\nSplitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Standardize the features
    print("Standardizing features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Test with original features (no PCA)
    print("\n" + "="*60)
    print("TRAINING SVM WITH ORIGINAL 30 FEATURES")
    print("="*60)
    
    svm_original = SVC(kernel='rbf', random_state=42)
    svm_original.fit(X_train_scaled, y_train)
    y_pred_original = svm_original.predict(X_test_scaled)
    
    acc_original = accuracy_score(y_test, y_pred_original)
    prec_original = precision_score(y_test, y_pred_original, average='weighted')
    rec_original = recall_score(y_test, y_pred_original, average='weighted')
    
    print(f"Accuracy:  {acc_original:.4f}")
    print(f"Precision: {prec_original:.4f}")
    print(f"Recall:    {rec_original:.4f}")
    
    # Store results
    results = []
    results.append({
        'n_components': 30,
        'accuracy': acc_original,
        'precision': prec_original,
        'recall': rec_original
    })
    
    # Test with different numbers of PCA components
    k_values = [2, 5, 10, 15]
    
    for k in k_values:
        print("\n" + "="*60)
        print(f"TRAINING SVM WITH {k} PRINCIPAL COMPONENTS")
        print("="*60)
        
        # Apply PCA
        pca = PCA(n_components=k)
        X_train_pca = pca.fit_transform(X_train_scaled)
        X_test_pca = pca.transform(X_test_scaled)
        
        variance_explained = sum(pca.explained_variance_ratio_)
        print(f"Variance explained by {k} PCs: {variance_explained:.4f}")
        
        # Train SVM
        svm = SVC(kernel='rbf', random_state=42)
        svm.fit(X_train_pca, y_train)
        y_pred = svm.predict(X_test_pca)
        
        # Calculate metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted')
        rec = recall_score(y_test, y_pred, average='weighted')
        
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall:    {rec:.4f}")
        
        results.append({
            'n_components': k,
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'variance_explained': variance_explained
        })
        
        # Save classification report
        report = classification_report(y_test, y_pred, target_names=data.target_names)
        with open(f'output/classification_report_{k}_components.txt', 'w') as f:
            f.write(f"Classification Report with {k} Principal Components\n")
            f.write("="*60 + "\n\n")
            f.write(report)
        
        # Plot confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=data.target_names, 
                   yticklabels=data.target_names)
        plt.title(f'Confusion Matrix - {k} PCs', fontsize=14, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.tight_layout()
        plt.savefig(f'output/confusion_matrix_{k}_components.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    results_df.to_csv('output/results_comparison.csv', index=False)
    
    print("\n" + "="*60)
    print("RESULTS COMPARISON")
    print("="*60)
    print(results_df.to_string(index=False))
    
    # Plot comparison
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    metrics = ['accuracy', 'precision', 'recall']
    titles = ['Accuracy vs Number of Components', 
             'Precision vs Number of Components',
             'Recall vs Number of Components']
    
    for idx, (metric, title) in enumerate(zip(metrics, titles)):
        ax = axes[idx]
        
        ax.plot(results_df['n_components'], results_df[metric], 
               marker='o', linestyle='-', linewidth=2, markersize=8, 
               color='steelblue', label=metric.capitalize())
        
        # Highlight original performance
        ax.axhline(y=results_df[results_df['n_components'] == 30][metric].values[0], 
                  color='red', linestyle='--', linewidth=2, 
                  label='Original (30 features)', alpha=0.7)
        
        ax.set_xlabel('Number of Principal Components', fontsize=12)
        ax.set_ylabel(metric.capitalize(), fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0.85, 1.0])
    
    plt.tight_layout()
    plt.savefig('output/metrics_comparison.png', dpi=300, bbox_inches='tight')
    print("\nMetrics comparison plot saved to output/metrics_comparison.png")
    plt.close()
    
    # Plot variance explained vs accuracy
    pca_results = results_df[results_df['n_components'] != 30]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('Number of Principal Components', fontsize=12)
    ax1.set_ylabel('Accuracy', color=color, fontsize=12)
    ax1.plot(pca_results['n_components'], pca_results['accuracy'], 
            marker='o', linestyle='-', linewidth=2, markersize=8, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Variance Explained', color=color, fontsize=12)
    ax2.plot(pca_results['n_components'], pca_results['variance_explained'], 
            marker='s', linestyle='--', linewidth=2, markersize=8, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Accuracy vs Variance Explained', fontsize=14, fontweight='bold')
    fig.tight_layout()
    plt.savefig('output/accuracy_vs_variance.png', dpi=300, bbox_inches='tight')
    print("Accuracy vs variance plot saved to output/accuracy_vs_variance.png")
    plt.close()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    best_k = results_df[results_df['n_components'] != 30].loc[
        results_df[results_df['n_components'] != 30]['accuracy'].idxmax()
    ]
    
    print(f"Best PCA configuration: {int(best_k['n_components'])} components")
    print(f"Best accuracy: {best_k['accuracy']:.4f}")
    print(f"Accuracy with all features: {acc_original:.4f}")
    print(f"Accuracy difference: {best_k['accuracy'] - acc_original:.4f}")
    
    # Save summary
    with open('output/summary.txt', 'w') as f:
        f.write("SVM Classification with PCA on Breast Cancer Dataset\n")
        f.write("="*60 + "\n\n")
        f.write(f"Original features: 30\n")
        f.write(f"Tested PCA components: {k_values}\n\n")
        f.write(f"Accuracy with all features: {acc_original:.4f}\n")
        f.write(f"Best PCA configuration: {int(best_k['n_components'])} components\n")
        f.write(f"Best PCA accuracy: {best_k['accuracy']:.4f}\n")
        f.write(f"Variance explained at best k: {best_k['variance_explained']:.4f}\n\n")
        f.write("Conclusion:\n")
        if best_k['accuracy'] >= acc_original:
            f.write(f"PCA with {int(best_k['n_components'])} components maintains or improves accuracy\n")
            f.write(f"while reducing dimensionality by {100 * (1 - best_k['n_components']/30):.1f}%\n")
        else:
            f.write(f"Best PCA accuracy is slightly lower but reduces dimensions by {100 * (1 - best_k['n_components']/30):.1f}%\n")
    
    print("\nAll results saved successfully!")
    print("="*60)

if __name__ == "__main__":
    evaluate_pca_svm()
