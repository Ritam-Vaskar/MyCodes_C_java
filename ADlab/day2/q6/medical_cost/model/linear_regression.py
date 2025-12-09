"""Linear Regression Model for Medical Cost Prediction"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

class MedicalCostPredictor:
    def __init__(self, normalize=True):
        self.model = LinearRegression()
        self.scaler = StandardScaler() if normalize else None
        self.normalize = normalize
        self.feature_names = None
        self.is_trained = False
        
    def train(self, X_train, y_train):
        print("\n[+] Training Medical Cost Predictor...")
        self.feature_names = X_train.columns.tolist() if isinstance(X_train, pd.DataFrame) else None
        X_array = X_train.values if isinstance(X_train, pd.DataFrame) else X_train
        X_scaled = self.scaler.fit_transform(X_array) if self.normalize else X_array
        self.model.fit(X_scaled, y_train)
        self.is_trained = True
        print(f"[+] Model trained! Features: {X_scaled.shape[1]}, Samples: {X_scaled.shape[0]}")
        
    def predict(self, X):
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        X_array = X.values if isinstance(X, pd.DataFrame) else X
        X_scaled = self.scaler.transform(X_array) if self.normalize else X_array
        return self.model.predict(X_scaled)
    
    def get_coefficients(self):
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        return pd.DataFrame({
            'Feature': self.feature_names or [f'Feature_{i}' for i in range(len(self.model.coef_))],
            'Coefficient': self.model.coef_,
            'Abs_Coefficient': np.abs(self.model.coef_)
        }).sort_values('Abs_Coefficient', ascending=False)
    
    def get_intercept(self):
        return self.model.intercept_ if self.is_trained else None
