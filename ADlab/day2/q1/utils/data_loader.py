"""
Data Loading Utilities for Boston Housing Dataset
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings('ignore')


def load_data():
    """
    Load Boston Housing Dataset
    Returns: X (features), y (target)
    """
    print("Loading Boston Housing Dataset...")
    
    # Load from online CSV source
    data_url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
    
    try:
        df = pd.read_csv(data_url)
        
        # Separate features and target
        X = df.drop('medv', axis=1)
        y = df['medv']
        
        print("Dataset loaded successfully!")
        print(f"Shape: {X.shape}")
        print(f"\nFeatures: {list(X.columns)}")
        print(f"\nTarget: medv (Median value of homes in $1000s)")
        
        return X, y
    
    except Exception as e:
        print(f"Error loading from online source: {e}")
        print("\nCreating sample dataset...")
        
        # Create sample dataset if online load fails
        from sklearn.datasets import make_regression
        X_sample, y_sample = make_regression(n_samples=506, n_features=13, noise=10, random_state=42)
        
        feature_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 
                        'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']
        
        X = pd.DataFrame(X_sample, columns=feature_names)
        y = pd.Series(y_sample, name='MEDV')
        
        print("Sample dataset created successfully!")
        
        return X, y


def split_data(X, y, test_size=0.2, random_state=42):
    """
    Split data into training and testing sets
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print(f"\nData split complete:")
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Testing set: {X_test.shape[0]} samples")
    
    return X_train, X_test, y_train, y_test


def get_data_statistics(X, y):
    """
    Get descriptive statistics of the dataset
    """
    print("\n" + "="*60)
    print("DATASET STATISTICS")
    print("="*60)
    
    print("\nFeature Statistics:")
    print(X.describe())
    
    print(f"\nTarget Variable Statistics:")
    print(f"Mean house price: ${y.mean():.2f}k")
    print(f"Median house price: ${y.median():.2f}k")
    print(f"Min house price: ${y.min():.2f}k")
    print(f"Max house price: ${y.max():.2f}k")
    print(f"Std deviation: ${y.std():.2f}k")
    
    print("\nMissing values:")
    print(X.isnull().sum())
    
    return X.describe(), y.describe()
