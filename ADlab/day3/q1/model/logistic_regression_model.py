"""
Spam Email Classifier using Logistic Regression
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns

class SpamClassifier:
    """
    Logistic Regression classifier for spam email detection.
    """
    
    def __init__(self):
        """Initialize the classifier with TF-IDF vectorizer and Logistic Regression model."""
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english', min_df=2, max_df=0.8)
        self.model = LogisticRegression(max_iter=1000, random_state=42, C=1.0)
        self.is_trained = False
    
    def train(self, X_train, y_train):
        """
        Train the spam classifier.
        
        Args:
            X_train: Training emails (list of strings)
            y_train: Training labels (0=non-spam, 1=spam)
        """
        # Convert text to TF-IDF features
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        
        # Train logistic regression model
        self.model.fit(X_train_tfidf, y_train)
        self.is_trained = True
    
    def predict(self, X_test):
        """
        Predict labels for test emails.
        
        Args:
            X_test: Test emails (list of strings)
        
        Returns:
            Predicted labels (0=non-spam, 1=spam)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions!")
        
        X_test_tfidf = self.vectorizer.transform(X_test)
        return self.model.predict(X_test_tfidf)
    
    def predict_proba(self, X_test):
        """
        Predict probability scores for test emails.
        
        Args:
            X_test: Test emails (list of strings)
        
        Returns:
            Probability scores for each class
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions!")
        
        X_test_tfidf = self.vectorizer.transform(X_test)
        return self.model.predict_proba(X_test_tfidf)
    
    def get_top_features(self, n=20):
        """
        Get the top features (words) that indicate spam.
        
        Args:
            n: Number of top features to return
        
        Returns:
            Dictionary with top spam and non-spam features
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first!")
        
        feature_names = self.vectorizer.get_feature_names_out()
        coefficients = self.model.coef_[0]
        
        # Get top spam indicators (positive coefficients)
        spam_indices = np.argsort(coefficients)[-n:]
        spam_features = [(feature_names[i], coefficients[i]) for i in spam_indices]
        
        # Get top non-spam indicators (negative coefficients)
        ham_indices = np.argsort(coefficients)[:n]
        ham_features = [(feature_names[i], coefficients[i]) for i in ham_indices]
        
        return {
            'spam_indicators': spam_features[::-1],
            'ham_indicators': ham_features
        }
    
    def visualize_results(self, X_test, y_test, y_pred, cm):
        """
        Create visualizations for model performance.
        
        Args:
            X_test: Test emails
            y_test: True labels
            y_pred: Predicted labels
            cm: Confusion matrix
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # 1. Confusion Matrix Heatmap
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Non-Spam', 'Spam'],
                    yticklabels=['Non-Spam', 'Spam'],
                    ax=axes[0, 0], cbar_kws={'label': 'Count'})
        axes[0, 0].set_title('Confusion Matrix', fontsize=14, fontweight='bold')
        axes[0, 0].set_ylabel('Actual Label', fontsize=12)
        axes[0, 0].set_xlabel('Predicted Label', fontsize=12)
        
        # 2. Class Distribution
        actual_counts = [np.sum(np.array(y_test) == 0), np.sum(np.array(y_test) == 1)]
        predicted_counts = [np.sum(np.array(y_pred) == 0), np.sum(np.array(y_pred) == 1)]
        
        x = np.arange(2)
        width = 0.35
        
        axes[0, 1].bar(x - width/2, actual_counts, width, label='Actual', color='skyblue')
        axes[0, 1].bar(x + width/2, predicted_counts, width, label='Predicted', color='lightcoral')
        axes[0, 1].set_xlabel('Class', fontsize=12)
        axes[0, 1].set_ylabel('Count', fontsize=12)
        axes[0, 1].set_title('Class Distribution', fontsize=14, fontweight='bold')
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(['Non-Spam', 'Spam'])
        axes[0, 1].legend()
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        # 3. Top Spam Indicators
        features = self.get_top_features(10)
        spam_words = [f[0] for f in features['spam_indicators']]
        spam_coefs = [f[1] for f in features['spam_indicators']]
        
        axes[1, 0].barh(spam_words, spam_coefs, color='orangered')
        axes[1, 0].set_xlabel('Coefficient', fontsize=12)
        axes[1, 0].set_title('Top 10 Spam Indicators', fontsize=14, fontweight='bold')
        axes[1, 0].grid(axis='x', alpha=0.3)
        
        # 4. Top Non-Spam Indicators
        ham_words = [f[0] for f in features['ham_indicators']]
        ham_coefs = [abs(f[1]) for f in features['ham_indicators']]
        
        axes[1, 1].barh(ham_words, ham_coefs, color='green')
        axes[1, 1].set_xlabel('Absolute Coefficient', fontsize=12)
        axes[1, 1].set_title('Top 10 Non-Spam Indicators', fontsize=14, fontweight='bold')
        axes[1, 1].grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('output/spam_classification_results.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("    ✓ Saved: spam_classification_results.png")
