"""
Q7: PCA for Spam Detection with TF-IDF Features
Objective: Reduce computational cost while maintaining spam detection accuracy
Pipeline: TF-IDF → PCA → SVM
Compare memory usage and accuracy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import sys
import os

def get_memory_usage(obj):
    """Get memory usage in MB"""
    return sys.getsizeof(obj) / (1024 * 1024)

def evaluate_spam_detection():
    """Evaluate spam detection with TF-IDF and PCA"""
    
    os.makedirs('output', exist_ok=True)
    
    print("="*70)
    print("SPAM DETECTION: TF-IDF → PCA → SVM PIPELINE")
    print("="*70)
    
    # Load dataset (using newsgroups as spam/ham proxy)
    print("\nLoading 20 newsgroups dataset...")
    categories = ['alt.atheism', 'talk.religion.misc', 'comp.graphics', 'sci.space']
    
    data_train = fetch_20newsgroups(subset='train', categories=categories,
                                    shuffle=True, random_state=42,
                                    remove=('headers', 'footers', 'quotes'))
    data_test = fetch_20newsgroups(subset='test', categories=categories,
                                   shuffle=True, random_state=42,
                                   remove=('headers', 'footers', 'quotes'))
    
    print(f"Training samples: {len(data_train.data)}")
    print(f"Test samples: {len(data_test.data)}")
    print(f"Categories: {data_train.target_names}")
    
    # Create TF-IDF features
    print("\n" + "="*70)
    print("CREATING TF-IDF FEATURES")
    print("="*70)
    
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english',
                                 max_df=0.5, min_df=2)
    X_train_tfidf = vectorizer.fit_transform(data_train.data)
    X_test_tfidf = vectorizer.transform(data_test.data)
    
    print(f"TF-IDF feature matrix shape: {X_train_tfidf.shape}")
    print(f"Number of features: {X_train_tfidf.shape[1]}")
    print(f"Matrix sparsity: {100*(1 - X_train_tfidf.nnz/(X_train_tfidf.shape[0]*X_train_tfidf.shape[1])):.2f}%")
    
    # Convert to dense for memory measurement (sparse matrices have different memory profile)
    X_train_dense = X_train_tfidf.toarray()
    X_test_dense = X_test_tfidf.toarray()
    
    memory_original = get_memory_usage(X_train_dense) + get_memory_usage(X_test_dense)
    print(f"Memory usage (dense): {memory_original:.2f} MB")
    
    y_train = data_train.target
    y_test = data_test.target
    
    # Train WITHOUT PCA
    print("\n" + "="*70)
    print("TRAINING WITHOUT PCA (5000 TF-IDF FEATURES)")
    print("="*70)
    
    svm_original = LinearSVC(random_state=42, max_iter=2000)
    svm_original.fit(X_train_dense, y_train)
    y_pred_original = svm_original.predict(X_test_dense)
    acc_original = accuracy_score(y_test, y_pred_original)
    
    print(f"Accuracy: {acc_original:.4f}")
    print(f"Memory usage: {memory_original:.2f} MB")
    
    results = [{
        'method': 'Original',
        'n_components': 5000,
        'accuracy': acc_original,
        'memory_mb': memory_original,
        'dimensionality_reduction_%': 0
    }]
    
    # Test with different PCA components
    pca_components = [50, 100, 200, 500, 1000]
    
    for n_comp in pca_components:
        print(f"\n{'='*70}")
        print(f"TRAINING WITH PCA ({n_comp} COMPONENTS)")
        print("="*70)
        
        # Apply PCA
        pca = PCA(n_components=n_comp, random_state=42)
        X_train_pca = pca.fit_transform(X_train_dense)
        X_test_pca = pca.transform(X_test_dense)
        
        variance_explained = sum(pca.explained_variance_ratio_)
        print(f"Variance explained: {variance_explained:.4f}")
        
        # Memory usage
        memory_pca = get_memory_usage(X_train_pca) + get_memory_usage(X_test_pca)
        memory_saving = 100 * (1 - memory_pca / memory_original)
        print(f"Memory usage: {memory_pca:.2f} MB")
        print(f"Memory saving: {memory_saving:.1f}%")
        
        # Train SVM
        svm = LinearSVC(random_state=42, max_iter=2000)
        svm.fit(X_train_pca, y_train)
        y_pred = svm.predict(X_test_pca)
        acc = accuracy_score(y_test, y_pred)
        
        print(f"Accuracy: {acc:.4f}")
        print(f"Accuracy difference: {acc - acc_original:+.4f}")
        
        results.append({
            'method': f'PCA-{n_comp}',
            'n_components': n_comp,
            'accuracy': acc,
            'memory_mb': memory_pca,
            'dimensionality_reduction_%': 100 * (1 - n_comp / 5000),
            'memory_saving_%': memory_saving,
            'variance_explained': variance_explained
        })
        
        # Save classification report
        report = classification_report(y_test, y_pred, 
                                      target_names=data_train.target_names)
        with open(f'output/classification_report_{n_comp}_components.txt', 'w') as f:
            f.write(f"Classification Report - PCA with {n_comp} Components\n")
            f.write("="*70 + "\n\n")
            f.write(report)
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    results_df.to_csv('output/results_comparison.csv', index=False)
    
    print("\n" + "="*70)
    print("COMPLETE RESULTS")
    print("="*70)
    print(results_df.to_string(index=False))
    
    # Plot accuracy vs memory
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sc = ax.scatter(results_df['memory_mb'], results_df['accuracy'],
                   s=300, c=results_df['n_components'], cmap='viridis',
                   alpha=0.7, edgecolors='black', linewidth=2)
    
    for idx, row in results_df.iterrows():
        method_label = f"{int(row['n_components'])}"
        ax.annotate(method_label, (row['memory_mb'], row['accuracy']),
                   xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Number of Components', fontsize=11)
    
    ax.set_xlabel('Memory Usage (MB)', fontsize=12)
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_title('Accuracy vs Memory Usage Trade-off', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/accuracy_vs_memory.png', dpi=300, bbox_inches='tight')
    print("\nAccuracy vs memory plot saved!")
    plt.close()
    
    # Multi-metric comparison
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Accuracy
    ax = axes[0, 0]
    ax.plot(results_df['n_components'], results_df['accuracy'],
           marker='o', linewidth=2, markersize=8, color='steelblue')
    ax.axhline(y=acc_original, color='red', linestyle='--', linewidth=2,
              label='Original', alpha=0.7)
    ax.set_xlabel('Number of Components', fontsize=12)
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_title('Accuracy vs Components', fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Memory usage
    ax = axes[0, 1]
    ax.plot(results_df['n_components'], results_df['memory_mb'],
           marker='s', linewidth=2, markersize=8, color='orange')
    ax.set_xlabel('Number of Components', fontsize=12)
    ax.set_ylabel('Memory Usage (MB)', fontsize=12)
    ax.set_title('Memory Usage vs Components', fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.grid(True, alpha=0.3)
    
    # Dimensionality reduction
    ax = axes[1, 0]
    ax.bar(range(len(results_df)), results_df['dimensionality_reduction_%'],
          color='lightgreen', edgecolor='darkgreen', alpha=0.7)
    ax.set_xlabel('Configuration', fontsize=12)
    ax.set_ylabel('Dimensionality Reduction (%)', fontsize=12)
    ax.set_title('Dimensionality Reduction', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(results_df)))
    ax.set_xticklabels([f"{int(r['n_components'])}" for _, r in results_df.iterrows()],
                       rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Memory savings
    ax = axes[1, 1]
    memory_savings = results_df[results_df['method'] != 'Original']['memory_saving_%']
    n_comps = results_df[results_df['method'] != 'Original']['n_components']
    ax.bar(range(len(memory_savings)), memory_savings,
          color='skyblue', edgecolor='navy', alpha=0.7)
    ax.set_xlabel('PCA Configuration', fontsize=12)
    ax.set_ylabel('Memory Savings (%)', fontsize=12)
    ax.set_title('Memory Savings with PCA', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(memory_savings)))
    ax.set_xticklabels([f"{int(n)}" for n in n_comps], rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('output/comprehensive_comparison.png', dpi=300, bbox_inches='tight')
    print("Comprehensive comparison plot saved!")
    plt.close()
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    best_tradeoff = results_df[results_df['method'] != 'Original'].loc[
        (results_df[results_df['method'] != 'Original']['accuracy'] >= 0.95 * acc_original).idxmax()
    ]
    
    print(f"\nOriginal Configuration:")
    print(f"  Features: 5000")
    print(f"  Accuracy: {acc_original:.4f}")
    print(f"  Memory: {memory_original:.2f} MB")
    
    print(f"\nBest Trade-off Configuration ({int(best_tradeoff['n_components'])} components):")
    print(f"  Accuracy: {best_tradeoff['accuracy']:.4f} ({100*best_tradeoff['accuracy']/acc_original:.1f}% of original)")
    print(f"  Memory: {best_tradeoff['memory_mb']:.2f} MB")
    print(f"  Memory savings: {best_tradeoff['memory_saving_%']:.1f}%")
    print(f"  Dimensionality reduction: {best_tradeoff['dimensionality_reduction_%']:.1f}%")
    
    # Save summary
    with open('output/summary.txt', 'w') as f:
        f.write("Spam Detection with TF-IDF and PCA\n")
        f.write("="*70 + "\n\n")
        f.write(f"Dataset: 20 Newsgroups (4 categories)\n")
        f.write(f"Training samples: {len(data_train.data)}\n")
        f.write(f"Test samples: {len(data_test.data)}\n\n")
        f.write(f"Original TF-IDF features: 5000\n")
        f.write(f"Original accuracy: {acc_original:.4f}\n")
        f.write(f"Original memory: {memory_original:.2f} MB\n\n")
        f.write(f"Best configuration: {int(best_tradeoff['n_components'])} components\n")
        f.write(f"  Accuracy: {best_tradeoff['accuracy']:.4f}\n")
        f.write(f"  Memory: {best_tradeoff['memory_mb']:.2f} MB\n")
        f.write(f"  Memory savings: {best_tradeoff['memory_saving_%']:.1f}%\n")
        f.write(f"  Dimensionality reduction: {best_tradeoff['dimensionality_reduction_%']:.1f}%\n\n")
        f.write("Conclusion:\n")
        f.write("PCA significantly reduces memory usage and computational cost\n")
        f.write("while maintaining competitive spam detection accuracy.\n")
    
    print("\nAll results saved successfully!")
    print("="*70)

if __name__ == "__main__":
    evaluate_spam_detection()
