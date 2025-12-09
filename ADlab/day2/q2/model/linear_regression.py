"""
Linear Regression Model for Advertising Analysis
"""

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd


class SalesPredictor:
    """
    Linear Regression model for sales prediction based on advertising spend
    """
    
    def __init__(self, normalize=True):
        """
        Initialize the model
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
        
        if self.normalize:
            X_train_scaled = self.scaler.fit_transform(X_train)
            print("[+] Feature normalization applied")
        else:
            X_train_scaled = X_train
        
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        print(f"[+] Model trained successfully")
        print(f"Number of features: {X_train.shape[1]}")
        print(f"Training samples: {X_train.shape[0]}")
        
        print(f"\nModel Intercept: {self.model.intercept_:.4f}")
        print(f"Number of coefficients: {len(self.model.coef_)}")
        
        return self
    
    def predict(self, X_test):
        """
        Make predictions on test data
        """
        if not self.is_trained:
            raise Exception("Model must be trained before making predictions!")
        
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
        
        equation = f"Sales = {self.model.intercept_:.4f}"
        
        for name, coef in zip(feature_names, self.model.coef_):
            sign = "+" if coef >= 0 else "-"
            equation += f" {sign} {abs(coef):.4f}*{name}"
        
        print(equation)
        print("="*60)
    
    def analyze_channel_impact(self, feature_names):
        """
        Analyze the impact of each advertising channel
        """
        print("\n" + "="*60)
        print("ADVERTISING CHANNEL IMPACT ANALYSIS")
        print("="*60)
        
        impacts = pd.DataFrame({
            'Channel': feature_names,
            'Coefficient': self.model.coef_,
            'Abs_Impact': np.abs(self.model.coef_)
        }).sort_values('Abs_Impact', ascending=False)
        
        print("\nChannel Effectiveness (Sales per $1000 spent):")
        print("-" * 60)
        
        for idx, row in impacts.iterrows():
            channel = row['Channel']
            coef = row['Coefficient']
            
            if coef > 0:
                print(f"{channel:12s}: +{coef:.4f}k units per $1k spent")
                print(f"              For every $1000 spent, sales increase by {coef*1000:.1f} units")
            else:
                print(f"{channel:12s}: {coef:.4f}k units per $1k spent")
                print(f"              Minimal or negative impact on sales")
            print()
        
        # ROI Analysis
        print("\nReturn on Investment (ROI) Ranking:")
        print("-" * 60)
        for i, (idx, row) in enumerate(impacts.iterrows(), 1):
            print(f"{i}. {row['Channel']:12s} (Coefficient: {row['Coefficient']:+.4f})")
        
        return impacts
