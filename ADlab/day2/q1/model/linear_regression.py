"""
Linear Regression Model Implementation
"""

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np


class HousePricePredictor:
    """
    Linear Regression model for house price prediction
    """
    
    def __init__(self, normalize=True):
        """
        Initialize the model
        Args:
            normalize: Whether to normalize features
        """
        self.model = LinearRegression()
        self.scaler = StandardScaler() if normalize else None
        self.normalize = normalize
        self.is_trained = False
    
    def train(self, X_train, y_train):
        """
        Train the linear regression model
        """
        print("\n" + "="*60)
        print("TRAINING LINEAR REGRESSION MODEL")
        print("="*60)
        
        # Normalize features if required
        if self.normalize:
            X_train_scaled = self.scaler.fit_transform(X_train)
            print("✓ Feature normalization applied")
        else:
            X_train_scaled = X_train
        
        # Train the model
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        print(f"✓ Model trained successfully")
        print(f"Number of features: {X_train.shape[1]}")
        print(f"Training samples: {X_train.shape[0]}")
        
        # Display model parameters
        print(f"\nModel Intercept: {self.model.intercept_:.4f}")
        print(f"Number of coefficients: {len(self.model.coef_)}")
        
        return self
    
    def predict(self, X_test):
        """
        Make predictions on test data
        """
        if not self.is_trained:
            raise Exception("Model must be trained before making predictions!")
        
        # Normalize if required
        if self.normalize:
            X_test_scaled = self.scaler.transform(X_test)
        else:
            X_test_scaled = X_test
        
        predictions = self.model.predict(X_test_scaled)
        
        return predictions
    
    def get_coefficients(self, feature_names):
        """
        Get feature coefficients with names
        """
        if not self.is_trained:
            raise Exception("Model must be trained first!")
        
        coef_dict = {
            'Intercept': self.model.intercept_
        }
        
        for name, coef in zip(feature_names, self.model.coef_):
            coef_dict[name] = coef
        
        return coef_dict
    
    def print_equation(self, feature_names):
        """
        Print the regression equation
        """
        print("\n" + "="*60)
        print("LINEAR REGRESSION EQUATION")
        print("="*60)
        
        equation = f"Price = {self.model.intercept_:.4f}"
        
        for name, coef in zip(feature_names, self.model.coef_):
            sign = "+" if coef >= 0 else "-"
            equation += f" {sign} {abs(coef):.4f}*{name}"
        
        print(equation)
        print("="*60)
    
    def get_top_features(self, feature_names, n=5):
        """
        Get top N most important features
        """
        import pandas as pd
        
        importance = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': self.model.coef_,
            'Abs_Coefficient': np.abs(self.model.coef_)
        }).sort_values('Abs_Coefficient', ascending=False)
        
        print(f"\nTop {n} Most Important Features:")
        print("-" * 50)
        for idx, row in importance.head(n).iterrows():
            impact = "increases" if row['Coefficient'] > 0 else "decreases"
            print(f"{row['Feature']:12s}: {row['Coefficient']:+.4f} ({impact} price)")
        
        return importance.head(n)
