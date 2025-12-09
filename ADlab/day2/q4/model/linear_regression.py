"""
Linear Regression Model for Student Performance Analysis
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

class StudentPerformancePredictor:
    """
    Linear Regression model for predicting student academic performance
    """
    
    def __init__(self, normalize=True):
        """
        Initialize the predictor
        
        Args:
            normalize (bool): Whether to normalize features
        """
        self.model = LinearRegression()
        self.scaler = StandardScaler() if normalize else None
        self.normalize = normalize
        self.feature_names = None
        self.is_trained = False
        
    def train(self, X_train, y_train):
        """
        Train the linear regression model
        
        Args:
            X_train (pd.DataFrame): Training features
            y_train (pd.Series): Training target
        """
        print("\n[+] Training Linear Regression Model...")
        
        # Store feature names
        if isinstance(X_train, pd.DataFrame):
            self.feature_names = X_train.columns.tolist()
            X_train_array = X_train.values
        else:
            X_train_array = X_train
            
        # Normalize features if required
        if self.normalize:
            X_train_scaled = self.scaler.fit_transform(X_train_array)
        else:
            X_train_scaled = X_train_array
            
        # Train the model
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        print(f"[+] Model trained successfully!")
        print(f"[+] Number of features: {X_train_scaled.shape[1]}")
        print(f"[+] Training samples: {X_train_scaled.shape[0]}")
        
    def predict(self, X):
        """
        Make predictions
        
        Args:
            X (pd.DataFrame): Features to predict
            
        Returns:
            np.ndarray: Predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
            
        # Convert to array if DataFrame
        if isinstance(X, pd.DataFrame):
            X_array = X.values
        else:
            X_array = X
            
        # Normalize if required
        if self.normalize:
            X_scaled = self.scaler.transform(X_array)
        else:
            X_scaled = X_array
            
        return self.model.predict(X_scaled)
    
    def get_coefficients(self):
        """
        Get model coefficients with feature names
        
        Returns:
            pd.DataFrame: Coefficients sorted by absolute value
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
            
        coef_df = pd.DataFrame({
            'Feature': self.feature_names if self.feature_names else [f'Feature_{i}' for i in range(len(self.model.coef_))],
            'Coefficient': self.model.coef_,
            'Abs_Coefficient': np.abs(self.model.coef_)
        })
        
        # Sort by absolute coefficient value
        coef_df = coef_df.sort_values('Abs_Coefficient', ascending=False)
        
        return coef_df
    
    def get_intercept(self):
        """
        Get model intercept
        
        Returns:
            float: Model intercept
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
            
        return self.model.intercept_
    
    def get_top_features(self, n=10):
        """
        Get top N most influential features
        
        Args:
            n (int): Number of top features to return
            
        Returns:
            pd.DataFrame: Top N features by absolute coefficient
        """
        coef_df = self.get_coefficients()
        return coef_df.head(n)
    
    def analyze_feature_groups(self, feature_groups):
        """
        Analyze impact of different feature groups
        
        Args:
            feature_groups (dict): Dictionary of feature group names to lists of features
            
        Returns:
            pd.DataFrame: Group-wise importance scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
            
        coef_df = self.get_coefficients()
        
        group_importance = []
        for group_name, features in feature_groups.items():
            # Get coefficients for features in this group
            group_coefs = coef_df[coef_df['Feature'].isin(features)]
            
            if len(group_coefs) > 0:
                avg_abs_coef = group_coefs['Abs_Coefficient'].mean()
                total_abs_coef = group_coefs['Abs_Coefficient'].sum()
                num_features = len(group_coefs)
                
                group_importance.append({
                    'Feature_Group': group_name,
                    'Num_Features': num_features,
                    'Avg_Abs_Coefficient': avg_abs_coef,
                    'Total_Abs_Coefficient': total_abs_coef
                })
        
        group_df = pd.DataFrame(group_importance)
        group_df = group_df.sort_values('Total_Abs_Coefficient', ascending=False)
        
        return group_df
    
    def predict_single_student(self, student_features):
        """
        Predict performance for a single student
        
        Args:
            student_features (dict or pd.Series): Student feature values
            
        Returns:
            float: Predicted grade
        """
        if isinstance(student_features, dict):
            student_df = pd.DataFrame([student_features])
        elif isinstance(student_features, pd.Series):
            student_df = student_features.to_frame().T
        else:
            student_df = student_features
            
        prediction = self.predict(student_df)
        return prediction[0]
