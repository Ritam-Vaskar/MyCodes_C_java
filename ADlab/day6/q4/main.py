"""
Q4: PCA Impact on Intrusion Detection - Accuracy and Latency Analysis
Objective: Analyze how PCA-based feature reduction impacts intrusion detection accuracy 
and detection latency. Measure training and prediction time, compare confusion matrices.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import time
import os

def create_intrusion_dataset():
    """Create synthetic intrusion detection dataset"""
    X, y = make_classification(
        n_samples=50000,
        n_features=40,
        n_informative=30,
        n_redundant=10,
        n_classes=2,
        weights=[0.8, 0.2],
        random_state=42
    )
    return X, y

def evaluate_intrusion_detection():
    """Evaluate intrusion detection with timing analysis"""
    
    os.makedirs('output', exist_ok=True)
    
    print("="*70)
    print("INTRUSION DETECTION WITH PCA - ACCURACY AND LATENCY ANALYSIS")
    print("="*70)
    
    # Create dataset
    print("\nCreating intrusion detection dataset...")
    X, y = create_intrusion_dataset()
    
    print(f"Dataset size: {X.shape}")
    print(f"Normal traffic: {np.sum(y==0)} samples")
    print(f"Intrusion attempts: {np.sum(y==1)} samples")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Standardize
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    results = []
    
    # Test WITHOUT PCA
    print("\n" + "="*70)
    print("EVALUATION WITHOUT PCA (40 FEATURES)")
    print("="*70)
    
    # Training time
    start_train = time.time()
    clf_original = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf_original.fit(X_train_scaled, y_train)
    train_time_original = time.time() - start_train
    
    # Prediction time
    start_pred = time.time()
    y_pred_original = clf_original.predict(X_test_scaled)
    pred_time_original = time.time() - start_pred
    
    acc_original = accuracy_score(y_test, y_pred_original)
    
    print(f"Training Time: {train_time_original:.4f} seconds")
    print(f"Prediction Time: {pred_time_original:.4f} seconds")
    print(f"Prediction Latency per sample: {1000*pred_time_original/len(X_test):.4f} ms")
    print(f"Accuracy: {acc_original:.4f}")
    
    results.append({
        'Method': 'Original',
        'n_components': 40,
        'train_time': train_time_original,
        'pred_time': pred_time_original,
        'latency_per_sample_ms': 1000*pred_time_original/len(X_test),
        'accuracy': acc_original
    })
    
    # Save confusion matrix
    cm_original = confusion_matrix(y_test, y_pred_original)
    
    # Test with different PCA components
    pca_components = [5, 10, 20, 30]
    
    for n_comp in pca_components:
        print(f"\n{'='*70}")
        print(f"EVALUATION WITH PCA ({n_comp} COMPONENTS)")
        print("="*70)
        
        # Apply PCA
        start_pca = time.time()
        pca = PCA(n_components=n_comp)
        X_train_pca = pca.fit_transform(X_train_scaled)
        X_test_pca = pca.transform(X_test_scaled)
        pca_time = time.time() - start_pca
        
        variance_explained = sum(pca.explained_variance_ratio_)
        print(f"PCA transformation time: {pca_time:.4f} seconds")
        print(f"Variance explained: {variance_explained:.4f}")
        
        # Training time
        start_train = time.time()
        clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        clf.fit(X_train_pca, y_train)
        train_time = time.time() - start_train
        
        # Prediction time
        start_pred = time.time()
        y_pred = clf.predict(X_test_pca)
        pred_time = time.time() - start_pred
        
        acc = accuracy_score(y_test, y_pred)
        
        print(f"Training Time: {train_time:.4f} seconds ({100*train_time/train_time_original:.1f}% of original)")
        print(f"Prediction Time: {pred_time:.4f} seconds ({100*pred_time/pred_time_original:.1f}% of original)")
        print(f"Prediction Latency per sample: {1000*pred_time/len(X_test):.4f} ms")
        print(f"Accuracy: {acc:.4f}")
        
        results.append({
            'Method': f'PCA-{n_comp}',
            'n_components': n_comp,
            'train_time': train_time,
            'pred_time': pred_time,
            'latency_per_sample_ms': 1000*pred_time/len(X_test),
            'accuracy': acc,
            'variance_explained': variance_explained
        })
        
        # Save confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Normal', 'Intrusion'],
                   yticklabels=['Normal', 'Intrusion'])
        plt.title(f'Confusion Matrix - {n_comp} PCs\nAccuracy: {acc:.4f}', 
                 fontsize=14, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.tight_layout()
        plt.savefig(f'output/confusion_matrix_{n_comp}_components.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    # Save original confusion matrix
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm_original, annot=True, fmt='d', cmap='Blues',
               xticklabels=['Normal', 'Intrusion'],
               yticklabels=['Normal', 'Intrusion'])
    plt.title(f'Confusion Matrix - Original (40 features)\nAccuracy: {acc_original:.4f}', 
             fontsize=14, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    plt.savefig('output/confusion_matrix_original.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    results_df.to_csv('output/timing_accuracy_results.csv', index=False)
    
    print("\n" + "="*70)
    print("RESULTS COMPARISON")
    print("="*70)
    print(results_df.to_string(index=False))
    
    # Plot comparisons
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Accuracy comparison
    ax = axes[0, 0]
    ax.plot(results_df['n_components'], results_df['accuracy'], 
           marker='o', linestyle='-', linewidth=2, markersize=8, color='steelblue')
    ax.axhline(y=acc_original, color='red', linestyle='--', linewidth=2, 
              label='Original', alpha=0.7)
    ax.set_xlabel('Number of Components', fontsize=12)
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_title('Accuracy vs Number of Components', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Training time comparison
    ax = axes[0, 1]
    ax.plot(results_df['n_components'], results_df['train_time'], 
           marker='s', linestyle='-', linewidth=2, markersize=8, color='orange')
    ax.set_xlabel('Number of Components', fontsize=12)
    ax.set_ylabel('Training Time (seconds)', fontsize=12)
    ax.set_title('Training Time vs Number of Components', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Prediction time comparison
    ax = axes[1, 0]
    ax.plot(results_df['n_components'], results_df['pred_time'], 
           marker='^', linestyle='-', linewidth=2, markersize=8, color='green')
    ax.set_xlabel('Number of Components', fontsize=12)
    ax.set_ylabel('Prediction Time (seconds)', fontsize=12)
    ax.set_title('Prediction Time vs Number of Components', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Latency per sample
    ax = axes[1, 1]
    ax.plot(results_df['n_components'], results_df['latency_per_sample_ms'], 
           marker='D', linestyle='-', linewidth=2, markersize=8, color='purple')
    ax.set_xlabel('Number of Components', fontsize=12)
    ax.set_ylabel('Latency per Sample (ms)', fontsize=12)
    ax.set_title('Detection Latency vs Number of Components', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/performance_comparison.png', dpi=300, bbox_inches='tight')
    print("\nPerformance comparison plots saved!")
    plt.close()
    
    # Accuracy vs Speed tradeoff
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sc = ax.scatter(results_df['latency_per_sample_ms'], results_df['accuracy'], 
                   s=200, c=results_df['n_components'], cmap='viridis', 
                   alpha=0.7, edgecolors='black', linewidth=2)
    
    for idx, row in results_df.iterrows():
        ax.annotate(f"{int(row['n_components'])} PCs", 
                   (row['latency_per_sample_ms'], row['accuracy']),
                   xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Number of Components', fontsize=11)
    
    ax.set_xlabel('Detection Latency per Sample (ms)', fontsize=12)
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_title('Accuracy vs Detection Latency Trade-off', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/accuracy_latency_tradeoff.png', dpi=300, bbox_inches='tight')
    print("Trade-off plot saved!")
    plt.close()
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    best_pca = results_df[results_df['Method'] != 'Original'].loc[
        results_df[results_df['Method'] != 'Original']['accuracy'].idxmax()
    ]
    
    speedup_train = train_time_original / best_pca['train_time']
    speedup_pred = pred_time_original / best_pca['pred_time']
    
    print(f"\nOriginal (40 features):")
    print(f"  Accuracy: {acc_original:.4f}")
    print(f"  Training time: {train_time_original:.4f}s")
    print(f"  Prediction time: {pred_time_original:.4f}s")
    print(f"  Latency per sample: {1000*pred_time_original/len(X_test):.4f}ms")
    
    print(f"\nBest PCA ({int(best_pca['n_components'])} components):")
    print(f"  Accuracy: {best_pca['accuracy']:.4f} (difference: {best_pca['accuracy']-acc_original:.4f})")
    print(f"  Training time: {best_pca['train_time']:.4f}s ({speedup_train:.2f}x speedup)")
    print(f"  Prediction time: {best_pca['pred_time']:.4f}s ({speedup_pred:.2f}x speedup)")
    print(f"  Latency per sample: {best_pca['latency_per_sample_ms']:.4f}ms")
    print(f"  Dimensionality reduction: {100*(1-best_pca['n_components']/40):.1f}%")
    
    # Save summary
    with open('output/summary.txt', 'w') as f:
        f.write("Intrusion Detection with PCA - Timing and Accuracy Analysis\n")
        f.write("="*70 + "\n\n")
        f.write(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features\n\n")
        f.write(f"Original Performance (40 features):\n")
        f.write(f"  Accuracy: {acc_original:.4f}\n")
        f.write(f"  Training time: {train_time_original:.4f}s\n")
        f.write(f"  Prediction time: {pred_time_original:.4f}s\n")
        f.write(f"  Latency per sample: {1000*pred_time_original/len(X_test):.4f}ms\n\n")
        
        f.write(f"Best PCA Configuration ({int(best_pca['n_components'])} components):\n")
        f.write(f"  Accuracy: {best_pca['accuracy']:.4f}\n")
        f.write(f"  Training speedup: {speedup_train:.2f}x\n")
        f.write(f"  Prediction speedup: {speedup_pred:.2f}x\n")
        f.write(f"  Latency reduction: {100*(1-best_pca['latency_per_sample_ms']/(1000*pred_time_original/len(X_test))):.1f}%\n")
        f.write(f"  Dimensionality reduction: {100*(1-best_pca['n_components']/40):.1f}%\n\n")
        
        f.write("Conclusion:\n")
        f.write(f"PCA reduces computational cost significantly while maintaining accuracy.\n")
        f.write(f"Optimal configuration achieves {speedup_pred:.2f}x faster predictions with minimal accuracy loss.\n")
    
    print("\nAll results saved successfully!")
    print("="*70)

if __name__ == "__main__":
    evaluate_intrusion_detection()
