"""
Data Loading Utilities for Advertising Dataset
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def load_data():
    """
    Load Advertising Dataset
    Returns: X (features), y (target)
    """
    print("Loading Advertising Dataset...")
    
    # Load from online source
    data_url = "https://raw.githubusercontent.com/selva86/datasets/master/Advertising.csv"
    
    try:
        df = pd.read_csv(data_url)
        
        # Remove index column if present
        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)
        
        # Separate features and target
        X = df[['TV', 'Radio', 'Newspaper']]
        y = df['Sales']
        
        print("Dataset loaded successfully!")
        print(f"Shape: {X.shape}")
        print(f"\nFeatures: {list(X.columns)}")
        print(f"Target: Sales (in thousands of units)")
        
        return X, y
    
    except Exception as e:
        print(f"Error loading from online source: {e}")
        print("\nCreating sample dataset...")
        
        # Create sample dataset if online load fails
        np.random.seed(42)
        n_samples = 200
        
        TV = np.random.uniform(0, 300, n_samples)
        Radio = np.random.uniform(0, 50, n_samples)
        Newspaper = np.random.uniform(0, 120, n_samples)
        
        # Sales with realistic relationship to advertising
        Sales = 7 + 0.05*TV + 0.1*Radio + 0.01*Newspaper + np.random.normal(0, 3, n_samples)
        
        X = pd.DataFrame({
            'TV': TV,
            'Radio': Radio,
            'Newspaper': Newspaper
        })
        y = pd.Series(Sales, name='Sales')
        
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
    
    print("\nAdvertising Budget Statistics:")
    print(X.describe())
    
    print(f"\nSales Statistics:")
    print(f"Mean sales: {y.mean():.2f}k units")
    print(f"Median sales: {y.median():.2f}k units")
    print(f"Min sales: {y.min():.2f}k units")
    print(f"Max sales: {y.max():.2f}k units")
    print(f"Std deviation: {y.std():.2f}k units")
    
    print("\nMissing values:")
    print(X.isnull().sum())
    
    return X.describe(), y.describe()


def analyze_correlations(X, y):
    """
    Analyze correlations between features and target
    """
    import pandas as pd
    
    print("\n" + "="*60)
    print("CORRELATION ANALYSIS")
    print("="*60)
    
    # Create dataframe with all variables
    data = X.copy()
    data['Sales'] = y
    
    # Calculate correlations with Sales
    correlations = data.corr()['Sales'].drop('Sales').sort_values(ascending=False)
    
    print("\nCorrelation with Sales:")
    for feature, corr in correlations.items():
        strength = "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.4 else "Weak"
        print(f"  {feature:12s}: {corr:+.4f} ({strength})")
    
    return correlations
