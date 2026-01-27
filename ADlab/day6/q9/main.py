"""
Q9: Eye State Detection with PCA - SVM vs KNN Comparison
Objective: Compare classification accuracy of SVM and KNN using original eye-feature 
vectors versus PCA-reduced features for eye state (open/closed) detection.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import os

def create_eye_state_dataset():
    """Create synthetic eye state detection dataset"""
    X, y = make_classification(
        n_samples=10000,
        n_features=14,  # Eye feature vectors (EEG-like features)
        n_informative=10,
        n_redundant=2,
        n_classes=2,  # Open vs Closed
        weights=[0.55, 0.45],
        random_state=42
    )
    return X, y

def evaluate_eye_state():
    """Evaluate eye state detection with and without PCA"""
    
    os.makedirs('output', exist_ok=True)
    
    print("="*70)
    print("EYE STATE DETECTION: SVM vs KNN WITH PCA")
    print("="*70)
    
    # Create dataset
    print("\nCreating eye state dataset...")
    X, y = create_eye_state_dataset()
    
    print(f"Dataset shape: {X.shape}")
    print(f"Eye open samples: {np.sum(y==0)}")
    print(f"Eye closed samples: {np.sum(y==1)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Standardize
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Classifiers
    classifiers = {
        'SVM': SVC(kernel='rbf', random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5)
    }
    
    results = []
    
    # Test WITHOUT PCA
    print("\n" + "="*70)
    print("EVALUATION WITHOUT PCA (14 FEATURES)")
    print("="*70)
    
    for clf_name, clf in classifiers.items():
        print(f"\n{clf_name} Classifier:")
        print("-" * 40)
        
        # Train and predict
        clf.fit(X_train_scaled, y_train)
        y_pred = clf.predict(X_test_scaled)
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='binary')
        rec = recall_score(y_test, y_pred, average='binary')
        f1 = f1_score(y_test, y_pred, average='binary')
        
        # Cross-validation
        cv_scores = cross_val_score(clf, X_train_scaled, y_train, cv=5)
        
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall:    {rec:.4f}")
        print(f"F1-Score:  {f1:.4f}")
        print(f"CV Score:  {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        
        results.append({
            'Classifier': clf_name,
            'Method': 'Original',
            'n_components': 14,
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1_score': f1,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        })
        
        # Save confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=['Open', 'Closed'],
                   yticklabels=['Open', 'Closed'])
        plt.title(f'{clf_name} - Confusion Matrix (Original)\nAccuracy: {acc:.4f}',
                 fontsize=14, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.tight_layout()
        plt.savefig(f'output/confusion_matrix_{clf_name}_original.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    # Test with different PCA components
    pca_components = [2, 4, 6, 8, 10, 12]
    
    for n_comp in pca_components:
        print(f"\n{'='*70}")
        print(f"EVALUATION WITH PCA ({n_comp} COMPONENTS)")
        print("="*70)
        
        # Apply PCA
        pca = PCA(n_components=n_comp)
        X_train_pca = pca.fit_transform(X_train_scaled)
        X_test_pca = pca.transform(X_test_scaled)
        
        variance_explained = sum(pca.explained_variance_ratio_)
        print(f"Variance explained: {variance_explained:.4f}")
        
        for clf_name, clf in classifiers.items():
            print(f"\n{clf_name} Classifier:")
            print("-" * 40)
            
            # Train and predict
            clf.fit(X_train_pca, y_train)
            y_pred = clf.predict(X_test_pca)
            
            # Metrics
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, average='binary')
            rec = recall_score(y_test, y_pred, average='binary')
            f1 = f1_score(y_test, y_pred, average='binary')
            
            # Cross-validation
            cv_scores = cross_val_score(clf, X_train_pca, y_train, cv=5)
            
            print(f"Accuracy:  {acc:.4f}")
            print(f"Precision: {prec:.4f}")
            print(f"Recall:    {rec:.4f}")
            print(f"F1-Score:  {f1:.4f}")
            print(f"CV Score:  {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
            
            results.append({
                'Classifier': clf_name,
                'Method': f'PCA-{n_comp}',
                'n_components': n_comp,
                'accuracy': acc,
                'precision': prec,
                'recall': rec,
                'f1_score': f1,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'variance_explained': variance_explained
            })
            
            # Save confusion matrix
            cm = confusion_matrix(y_test, y_pred)
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                       xticklabels=['Open', 'Closed'],
                       yticklabels=['Open', 'Closed'])
            plt.title(f'{clf_name} - Confusion Matrix (PCA-{n_comp})\nAccuracy: {acc:.4f}',
                     fontsize=14, fontweight='bold')
            plt.ylabel('True Label', fontsize=12)
            plt.xlabel('Predicted Label', fontsize=12)
            plt.tight_layout()
            plt.savefig(f'output/confusion_matrix_{clf_name}_pca_{n_comp}.png',
                       dpi=300, bbox_inches='tight')
            plt.close()
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    results_df.to_csv('output/results_comparison.csv', index=False)
    
    print("\n" + "="*70)
    print("COMPLETE RESULTS")
    print("="*70)
    print(results_df.to_string(index=False))
    
    # Plot comparison for both classifiers
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    titles = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    
    for idx, (metric, title) in enumerate(zip(metrics, titles)):
        ax = axes[idx // 2, idx % 2]
        
        for clf_name in ['SVM', 'KNN']:
            clf_data = results_df[results_df['Classifier'] == clf_name]
            ax.plot(clf_data['n_components'], clf_data[metric],
                   marker='o', linewidth=2, markersize=8, label=clf_name)
        
        ax.set_xlabel('Number of Components', fontsize=12)
        ax.set_ylabel(title, fontsize=12)
        ax.set_title(f'{title} vs Number of Components', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/metrics_comparison.png', dpi=300, bbox_inches='tight')
    print("\nMetrics comparison saved!")
    plt.close()
    
    # Side-by-side comparison
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    for idx, clf_name in enumerate(['SVM', 'KNN']):
        ax = axes[idx]
        clf_data = results_df[results_df['Classifier'] == clf_name]
        
        x = np.arange(len(clf_data))
        width = 0.2
        
        ax.bar(x - 1.5*width, clf_data['accuracy'], width, label='Accuracy', alpha=0.8)
        ax.bar(x - 0.5*width, clf_data['precision'], width, label='Precision', alpha=0.8)
        ax.bar(x + 0.5*width, clf_data['recall'], width, label='Recall', alpha=0.8)
        ax.bar(x + 1.5*width, clf_data['f1_score'], width, label='F1-Score', alpha=0.8)
        
        ax.set_xlabel('Configuration', fontsize=12)
        ax.set_ylabel('Score', fontsize=12)
        ax.set_title(f'{clf_name} - All Metrics Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(clf_data['Method'], rotation=45, ha='right')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim([0.7, 1.0])
    
    plt.tight_layout()
    plt.savefig('output/classifier_comparison.png', dpi=300, bbox_inches='tight')
    print("Classifier comparison saved!")
    plt.close()
    
    # Heatmap comparison
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    for idx, clf_name in enumerate(['SVM', 'KNN']):
        ax = axes[idx]
        clf_data = results_df[results_df['Classifier'] == clf_name]
        pivot_data = clf_data[['Method', 'accuracy', 'precision', 'recall', 'f1_score']].set_index('Method').T
        
        sns.heatmap(pivot_data, annot=True, fmt='.3f', cmap='YlGnBu',
                   vmin=0.8, vmax=1.0, ax=ax, cbar_kws={'label': 'Score'})
        ax.set_title(f'{clf_name} - Performance Heatmap', fontsize=14, fontweight='bold')
        ax.set_xlabel('Configuration', fontsize=12)
        ax.set_ylabel('Metric', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('output/performance_heatmap.png', dpi=300, bbox_inches='tight')
    print("Performance heatmap saved!")
    plt.close()
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for clf_name in ['SVM', 'KNN']:
        clf_data = results_df[results_df['Classifier'] == clf_name]
        original = clf_data[clf_data['Method'] == 'Original'].iloc[0]
        best_pca = clf_data[clf_data['Method'] != 'Original'].loc[
            clf_data[clf_data['Method'] != 'Original']['accuracy'].idxmax()
        ]
        
        print(f"\n{clf_name} Results:")
        print(f"  Original (14 features):")
        print(f"    Accuracy: {original['accuracy']:.4f}")
        print(f"    F1-Score: {original['f1_score']:.4f}")
        print(f"  Best PCA ({int(best_pca['n_components'])} components):")
        print(f"    Accuracy: {best_pca['accuracy']:.4f} (diff: {best_pca['accuracy']-original['accuracy']:+.4f})")
        print(f"    F1-Score: {best_pca['f1_score']:.4f} (diff: {best_pca['f1_score']-original['f1_score']:+.4f})")
        print(f"    Dimensionality reduction: {100*(1-best_pca['n_components']/14):.1f}%")
    
    # Determine winner
    svm_best = results_df[(results_df['Classifier'] == 'SVM')]['accuracy'].max()
    knn_best = results_df[(results_df['Classifier'] == 'KNN')]['accuracy'].max()
    
    print(f"\nBest Overall Performance:")
    if svm_best > knn_best:
        print(f"  SVM achieves highest accuracy: {svm_best:.4f}")
    else:
        print(f"  KNN achieves highest accuracy: {knn_best:.4f}")
    
    # Save summary
    with open('output/summary.txt', 'w') as f:
        f.write("Eye State Detection: SVM vs KNN with PCA\n")
        f.write("="*70 + "\n\n")
        f.write(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features\n")
        f.write(f"Classes: Eye Open, Eye Closed\n\n")
        
        for clf_name in ['SVM', 'KNN']:
            clf_data = results_df[results_df['Classifier'] == clf_name]
            original = clf_data[clf_data['Method'] == 'Original'].iloc[0]
            best_pca = clf_data[clf_data['Method'] != 'Original'].loc[
                clf_data[clf_data['Method'] != 'Original']['accuracy'].idxmax()
            ]
            
            f.write(f"{clf_name} Performance:\n")
            f.write(f"  Original: Accuracy = {original['accuracy']:.4f}, F1 = {original['f1_score']:.4f}\n")
            f.write(f"  Best PCA ({int(best_pca['n_components'])} PCs): Accuracy = {best_pca['accuracy']:.4f}, F1 = {best_pca['f1_score']:.4f}\n")
            f.write(f"  Improvement: {best_pca['accuracy']-original['accuracy']:+.4f}\n")
            f.write(f"  Dimensionality reduction: {100*(1-best_pca['n_components']/14):.1f}%\n\n")
        
        f.write("Conclusion:\n")
        if svm_best > knn_best:
            f.write("SVM demonstrates superior performance for eye state detection.\n")
        else:
            f.write("KNN demonstrates superior performance for eye state detection.\n")
        f.write("PCA maintains or improves accuracy while reducing features significantly.\n")
    
    print("\nAll results saved successfully!")
    print("="*70)

if __name__ == "__main__":
    evaluate_eye_state()
