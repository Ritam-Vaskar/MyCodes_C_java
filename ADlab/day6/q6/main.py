"""
Q6: PCA Robustness Analysis with Noisy Clinical Features
Objective: Evaluate if PCA improves classification stability and accuracy under 
noisy clinical feature conditions using SVM models.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import os

def add_noise(X, noise_level=0.1):
    """Add Gaussian noise to features"""
    noise = np.random.normal(0, noise_level, X.shape)
    return X + noise * np.std(X, axis=0)

def evaluate_robustness():
    """Evaluate PCA robustness with noisy features"""
    
    os.makedirs('output', exist_ok=True)
    
    print("="*70)
    print("PCA ROBUSTNESS ANALYSIS WITH NOISY CLINICAL FEATURES")
    print("="*70)
    
    # Load dataset
    print("\nLoading Breast Cancer dataset...")
    data = load_breast_cancer()
    X = data.data
    y = data.target
    
    print(f"Dataset shape: {X.shape}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Standardize
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Test different noise levels
    noise_levels = [0.0, 0.1, 0.2, 0.3, 0.5, 1.0]
    pca_components = [0, 10, 15, 20]  # 0 means no PCA
    
    results = []
    
    for noise in noise_levels:
        print(f"\n{'='*70}")
        print(f"NOISE LEVEL: {noise}")
        print("="*70)
        
        # Add noise
        X_train_noisy = add_noise(X_train_scaled, noise)
        X_test_noisy = add_noise(X_test_scaled, noise)
        
        for n_comp in pca_components:
            if n_comp == 0:
                # No PCA
                X_train_proc = X_train_noisy
                X_test_proc = X_test_noisy
                method = 'Original'
            else:
                # With PCA
                pca = PCA(n_components=n_comp)
                X_train_proc = pca.fit_transform(X_train_noisy)
                X_test_proc = pca.transform(X_test_noisy)
                method = f'PCA-{n_comp}'
            
            # Train SVM
            svm = SVC(kernel='rbf', random_state=42)
            svm.fit(X_train_proc, y_train)
            
            # Evaluate
            acc = accuracy_score(y_test, svm.predict(X_test_proc))
            
            # Cross-validation for stability
            cv_scores = cross_val_score(svm, X_train_proc, y_train, cv=5)
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()
            
            results.append({
                'noise_level': noise,
                'method': method,
                'n_components': n_comp if n_comp > 0 else 30,
                'test_accuracy': acc,
                'cv_mean': cv_mean,
                'cv_std': cv_std
            })
            
            print(f"{method:12s} | Acc: {acc:.4f} | CV: {cv_mean:.4f} ± {cv_std:.4f}")
    
    # Create DataFrame
    results_df = pd.DataFrame(results)
    results_df.to_csv('output/robustness_results.csv', index=False)
    
    print("\n" + "="*70)
    print("COMPLETE RESULTS")
    print("="*70)
    print(results_df.to_string(index=False))
    
    # Plot accuracy vs noise level
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Test accuracy
    ax = axes[0]
    for method in results_df['method'].unique():
        method_data = results_df[results_df['method'] == method]
        ax.plot(method_data['noise_level'], method_data['test_accuracy'],
               marker='o', linewidth=2, markersize=8, label=method)
    
    ax.set_xlabel('Noise Level', fontsize=12)
    ax.set_ylabel('Test Accuracy', fontsize=12)
    ax.set_title('Test Accuracy vs Noise Level', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Cross-validation stability
    ax = axes[1]
    for method in results_df['method'].unique():
        method_data = results_df[results_df['method'] == method]
        ax.errorbar(method_data['noise_level'], method_data['cv_mean'],
                   yerr=method_data['cv_std'], marker='o', linewidth=2,
                   markersize=8, capsize=5, label=method)
    
    ax.set_xlabel('Noise Level', fontsize=12)
    ax.set_ylabel('Cross-Validation Accuracy', fontsize=12)
    ax.set_title('CV Accuracy vs Noise Level (with std)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/accuracy_vs_noise.png', dpi=300, bbox_inches='tight')
    print("\nAccuracy plots saved!")
    plt.close()
    
    # Stability analysis - CV std dev
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for method in results_df['method'].unique():
        method_data = results_df[results_df['method'] == method]
        ax.plot(method_data['noise_level'], method_data['cv_std'],
               marker='s', linewidth=2, markersize=8, label=method)
    
    ax.set_xlabel('Noise Level', fontsize=12)
    ax.set_ylabel('CV Standard Deviation', fontsize=12)
    ax.set_title('Model Stability (Lower is Better)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/stability_analysis.png', dpi=300, bbox_inches='tight')
    print("Stability plot saved!")
    plt.close()
    
    # Heatmap of accuracy degradation
    pivot_df = results_df.pivot(index='method', columns='noise_level', values='test_accuracy')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot_df, annot=True, fmt='.3f', cmap='RdYlGn', 
               vmin=0.8, vmax=1.0, cbar_kws={'label': 'Accuracy'})
    plt.title('Accuracy Heatmap: Method vs Noise Level', fontsize=14, fontweight='bold')
    plt.xlabel('Noise Level', fontsize=12)
    plt.ylabel('Method', fontsize=12)
    plt.tight_layout()
    plt.savefig('output/accuracy_heatmap.png', dpi=300, bbox_inches='tight')
    print("Heatmap saved!")
    plt.close()
    
    # Performance degradation analysis
    baseline_df = results_df[results_df['noise_level'] == 0.0].set_index('method')['test_accuracy']
    
    degradation_data = []
    for method in results_df['method'].unique():
        method_data = results_df[results_df['method'] == method]
        baseline = baseline_df[method]
        
        for _, row in method_data.iterrows():
            if row['noise_level'] > 0:
                degradation = baseline - row['test_accuracy']
                degradation_data.append({
                    'method': method,
                    'noise_level': row['noise_level'],
                    'degradation': degradation
                })
    
    degrad_df = pd.DataFrame(degradation_data)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    for method in degrad_df['method'].unique():
        method_data = degrad_df[degrad_df['method'] == method]
        ax.plot(method_data['noise_level'], method_data['degradation'],
               marker='o', linewidth=2, markersize=8, label=method)
    
    ax.set_xlabel('Noise Level', fontsize=12)
    ax.set_ylabel('Accuracy Degradation', fontsize=12)
    ax.set_title('Accuracy Degradation from Baseline (Lower is Better)', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/degradation_analysis.png', dpi=300, bbox_inches='tight')
    print("Degradation plot saved!")
    plt.close()
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    # Find most robust method
    avg_degradation = degrad_df.groupby('method')['degradation'].mean()
    most_robust = avg_degradation.idxmin()
    
    print(f"\nMost robust method: {most_robust}")
    print(f"Average degradation: {avg_degradation[most_robust]:.4f}")
    
    print("\nStability ranking (by average CV std):")
    stability_ranking = results_df[results_df['noise_level'] > 0].groupby('method')['cv_std'].mean().sort_values()
    for i, (method, std) in enumerate(stability_ranking.items(), 1):
        print(f"  {i}. {method}: {std:.4f}")
    
    # Save summary
    with open('output/summary.txt', 'w') as f:
        f.write("PCA Robustness Analysis with Noisy Clinical Features\n")
        f.write("="*70 + "\n\n")
        f.write("Dataset: Breast Cancer (30 features)\n")
        f.write(f"Noise levels tested: {noise_levels}\n")
        f.write(f"PCA configurations: {pca_components}\n\n")
        
        f.write(f"Most robust method: {most_robust}\n")
        f.write(f"Average accuracy degradation: {avg_degradation[most_robust]:.4f}\n\n")
        
        f.write("Stability ranking (lower std = more stable):\n")
        for i, (method, std) in enumerate(stability_ranking.items(), 1):
            f.write(f"  {i}. {method}: CV std = {std:.4f}\n")
        
        f.write("\nConclusion:\n")
        if 'PCA' in most_robust:
            f.write("PCA improves model robustness under noisy conditions.\n")
            f.write("Dimensionality reduction acts as noise filter, improving stability.\n")
        else:
            f.write("Original features perform better, but PCA provides competitive results.\n")
    
    print("\nAll results saved successfully!")
    print("="*70)

if __name__ == "__main__":
    evaluate_robustness()
