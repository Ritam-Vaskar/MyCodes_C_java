"""
Linear Regression Model for Time Series Forecasting
"""

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd


class TimeSeriesPredictor:
    """
    Linear Regression model for time series forecasting
    """
    
    def __init__(self, normalize=True):
        """
        Initialize the model
        """
        self.model = LinearRegression()
        self.scaler = StandardScaler() if normalize else None
        self.normalize = normalize
        self.is_trained = False
        self.feature_names = None
    
    def train(self, X_train, y_train, feature_names):
        """
        Train the time series forecasting model
        """
        print("\n" + "="*60)
        print("TRAINING TIME SERIES MODEL")
        print("="*60)
        
        self.feature_names = feature_names
        
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
    
    def forecast_future(self, last_date, n_days):
        """
        Forecast future values
        """
        from datetime import timedelta
        
        if not self.is_trained:
            raise Exception("Model must be trained first!")
        
        print(f"\n[+] Generating {n_days}-day forecast...")
        
        # Generate future dates
        future_dates = [last_date + timedelta(days=i+1) for i in range(n_days)]
        
        # Create feature dataframe
        future_df = pd.DataFrame({'Date': future_dates})
        future_df['DayOfYear'] = future_df['Date'].dt.dayofyear
        future_df['Year'] = future_df['Date'].dt.year
        future_df['Month'] = future_df['Date'].dt.month
        future_df['DayOfWeek'] = future_df['Date'].dt.dayofweek
        future_df['Sin_DayOfYear'] = np.sin(2 * np.pi * future_df['DayOfYear'] / 365.25)
        future_df['Cos_DayOfYear'] = np.cos(2 * np.pi * future_df['DayOfYear'] / 365.25)
        
        # TimeIndex continues from last training point
        last_time_index = self.last_time_index if hasattr(self, 'last_time_index') else 0
        future_df['TimeIndex'] = range(last_time_index + 1, last_time_index + n_days + 1)
        
        # Extract features
        X_future = future_df[self.feature_names].values
        
        # Predict
        predictions = self.predict(X_future)
        
        future_df['Predicted_Temperature'] = predictions
        
        return future_df
    
    def analyze_components(self):
        """
        Analyze trend and seasonal components
        """
        print("\n" + "="*60)
        print("MODEL COMPONENT ANALYSIS")
        print("="*60)
        
        # Get coefficients
        coef_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Coefficient': self.model.coef_
        })
        
        # Identify trend component
        if 'TimeIndex' in self.feature_names:
            trend_idx = self.feature_names.index('TimeIndex')
            trend_coef = self.model.coef_[trend_idx]
            print(f"\nTrend Component:")
            print(f"  TimeIndex coefficient: {trend_coef:.6f}°/day")
            
            if abs(trend_coef) < 0.001:
                print(f"  Interpretation: No significant trend")
            elif trend_coef > 0:
                print(f"  Interpretation: Temperature increasing by {trend_coef*365:.4f}°/year")
            else:
                print(f"  Interpretation: Temperature decreasing by {abs(trend_coef*365):.4f}°/year")
        
        # Identify seasonal components
        seasonal_features = ['Sin_DayOfYear', 'Cos_DayOfYear']
        print(f"\nSeasonal Components:")
        for feat in seasonal_features:
            if feat in self.feature_names:
                idx = self.feature_names.index(feat)
                print(f"  {feat}: {self.model.coef_[idx]:.4f}")
        
        return coef_df
    
    def print_equation(self):
        """
        Print the regression equation
        """
        print("\n" + "="*60)
        print("TIME SERIES REGRESSION EQUATION")
        print("="*60)
        
        equation = f"Temperature = {self.model.intercept_:.4f}"
        
        for name, coef in zip(self.feature_names, self.model.coef_):
            sign = "+" if coef >= 0 else "-"
            equation += f" {sign} {abs(coef):.4f}*{name}"
        
        print(equation)
        print("="*60)
    
    def set_last_time_index(self, value):
        """
        Set the last time index for forecasting
        """
        self.last_time_index = value
