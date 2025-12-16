"""
Iris Species Classifier using Decision Tree
"""

import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns

class IrisClassifier:
    """
    Decision Tree classifier for Iris species classification.
    """
    
    def __init__(self, max_depth=4, random_state=42):
        """
        Initialize the classifier.
        
        Args:
            max_depth: Maximum depth of the decision tree
            random_state: Random seed for reproducibility
        """
        self.model = DecisionTreeClassifier(
            max_depth=max_depth,
            random_state=random_state,
            criterion='gini'
        )
        self.is_trained = False
    
    def train(self, X_train, y_train):
        """
        Train the decision tree classifier.
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        self.model.fit(X_train, y_train)
        self.is_trained = True
    
    def predict(self, X_test):
        """
        Predict labels for test samples.
        
        Args:
            X_test: Test features
        
        Returns:
            Predicted labels
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions!")
        
        return self.model.predict(X_test)
    
    def predict_proba(self, X_test):
        """
        Predict probability scores for test samples.
        
        Args:
            X_test: Test features
        
        Returns:
            Probability scores for each class
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions!")
        
        return self.model.predict_proba(X_test)
    
    def get_feature_importance(self):
        """
        Get feature importance scores.
        
        Returns:
            List of tuples (feature_name, importance_score)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first!")
        
        return [(f"Feature {i}", imp) for i, imp in enumerate(self.model.feature_importances_)]
    
    def visualize_tree(self, feature_names, class_names):
        """
        Visualize the decision tree structure using plot_tree().
        
        Args:
            feature_names: Names of features
            class_names: Names of classes
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first!")
        
        plt.figure(figsize=(20, 12))
        plot_tree(self.model, 
                  feature_names=feature_names,
                  class_names=class_names,
                  filled=True,
                  rounded=True,
                  fontsize=10)
        plt.title('Decision Tree for Iris Classification', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('output/decision_tree_structure.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("    ✓ Saved: decision_tree_structure.png")
    
    def visualize_results(self, X_test, y_test, y_pred, cm, feature_names, class_names):
        """
        Create visualizations for model performance.
        
        Args:
            X_test: Test features
            y_test: True labels
            y_pred: Predicted labels
            cm: Confusion matrix
            feature_names: Names of features
            class_names: Names of classes
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # 1. Confusion Matrix Heatmap
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=class_names,
                    yticklabels=class_names,
                    ax=axes[0, 0], cbar_kws={'label': 'Count'})
        axes[0, 0].set_title('Confusion Matrix', fontsize=14, fontweight='bold')
        axes[0, 0].set_ylabel('Actual Species', fontsize=12)
        axes[0, 0].set_xlabel('Predicted Species', fontsize=12)
        
        # 2. Class Distribution
        actual_counts = [sum(y_test == i) for i in range(len(class_names))]
        predicted_counts = [sum(y_pred == i) for i in range(len(class_names))]
        
        x = np.arange(len(class_names))
        width = 0.35
        
        axes[0, 1].bar(x - width/2, actual_counts, width, label='Actual', color='skyblue')
        axes[0, 1].bar(x + width/2, predicted_counts, width, label='Predicted', color='lightcoral')
        axes[0, 1].set_xlabel('Species', fontsize=12)
        axes[0, 1].set_ylabel('Count', fontsize=12)
        axes[0, 1].set_title('Class Distribution', fontsize=14, fontweight='bold')
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(class_names, rotation=45)
        axes[0, 1].legend()
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        # 3. Feature Importance
        importances = self.model.feature_importances_
        indices = np.argsort(importances)
        
        axes[1, 0].barh([feature_names[i] for i in indices], 
                        importances[indices], 
                        color='green')
        axes[1, 0].set_xlabel('Importance', fontsize=12)
        axes[1, 0].set_title('Feature Importance', fontsize=14, fontweight='bold')
        axes[1, 0].grid(axis='x', alpha=0.3)
        
        # 4. Pairwise Feature Scatter (Petal Length vs Petal Width)
        colors = ['red', 'blue', 'green']
        for i, class_name in enumerate(class_names):
            mask = y_test == i
            axes[1, 1].scatter(X_test[mask, 2], X_test[mask, 3],
                             c=colors[i], label=class_name, alpha=0.6, s=50)
        
        # Plot misclassifications
        misclassified = y_test != y_pred
        if np.any(misclassified):
            axes[1, 1].scatter(X_test[misclassified, 2], X_test[misclassified, 3],
                             c='black', marker='x', s=100, linewidths=2,
                             label='Misclassified')
        
        axes[1, 1].set_xlabel(feature_names[2], fontsize=12)
        axes[1, 1].set_ylabel(feature_names[3], fontsize=12)
        axes[1, 1].set_title('Petal Dimensions (Misclassifications marked with X)', 
                            fontsize=14, fontweight='bold')
        axes[1, 1].legend()
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('output/iris_classification_results.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("    ✓ Saved: iris_classification_results.png")
