"""
Linear Regression Model for Car Mileage Prediction
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

class MPGPredictor:
    """Linear Regression model for predicting car MPG"""
    
    def __init__(self, normalize=True):
        self.model = LinearRegression()
        self.scaler = StandardScaler() if normalize else None
        self.normalize = normalize
        self.feature_names = None
        self.is_trained = False
        
    def train(self, X_train, y_train):
        print("\n[+] Training MPG Predictor...")
        
        if isinstance(X_train, pd.DataFrame):
            self.feature_names = X_train.columns.tolist()
            X_train_array = X_train.values
        else:
            X_train_array = X_train
            
        if self.normalize:
            X_train_scaled = self.scaler.fit_transform(X_train_array)
        else:
            X_train_scaled = X_train_array
            
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        print(f"[+] Model trained successfully!")
        print(f"[+] Features: {X_train_scaled.shape[1]}")
        print(f"[+] Training samples: {X_train_scaled.shape[0]}")
        
    def predict(self, X):
        if not self.is_trained:
            raise ValueError("Model must be trained first")
            
        X_array = X.values if isinstance(X, pd.DataFrame) else X
        X_scaled = self.scaler.transform(X_array) if self.normalize else X_array
        return self.model.predict(X_scaled)
    
    def get_coefficients(self):
        if not self.is_trained:
            raise ValueError("Model must be trained first")
            
        coef_df = pd.DataFrame({
            'Feature': self.feature_names if self.feature_names else [f'Feature_{i}' for i in range(len(self.model.coef_))],
            'Coefficient': self.model.coef_,
            'Abs_Coefficient': np.abs(self.model.coef_)
        })
        
        return coef_df.sort_values('Abs_Coefficient', ascending=False)
    
    def get_intercept(self):
        return self.model.intercept_ if self.is_trained else None
