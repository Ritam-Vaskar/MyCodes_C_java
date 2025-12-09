"""
Data loading utilities for Auto MPG Dataset
"""
import pandas as pd
import numpy as np

def load_auto_mpg_data():
    """
    Load the Auto MPG Dataset from UCI ML Repository
    
    Returns:
        pd.DataFrame: Loaded auto MPG data
    """
    print("[+] Loading Auto MPG Dataset...")
    
    try:
        # UCI ML Repository - Auto MPG Dataset
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
        
        # Column names from dataset documentation
        column_names = [
            'mpg', 'cylinders', 'displacement', 'horsepower', 'weight',
            'acceleration', 'model_year', 'origin', 'car_name'
        ]
        
        # Load data with proper delimiter (whitespace)
        df = pd.read_csv(url, delim_whitespace=True, names=column_names, na_values='?')
        
        print(f"[+] Dataset loaded successfully!")
        print(f"[+] Shape: {df.shape}")
        print(f"[+] Columns: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"[!] Error loading from UCI: {e}")
        print(f"[+] Creating synthetic Auto MPG dataset...")
        return create_synthetic_auto_mpg(n_samples=398)

def create_synthetic_auto_mpg(n_samples=398):
    """
    Create synthetic Auto MPG dataset for demonstration
    
    Args:
        n_samples (int): Number of cars to generate
        
    Returns:
        pd.DataFrame: Synthetic auto data
    """
    np.random.seed(42)
    
    print(f"[+] Generating synthetic dataset with {n_samples} cars...")
    
    # Generate realistic car attributes
    cylinders = np.random.choice([4, 6, 8], n_samples, p=[0.5, 0.3, 0.2])
    
    data = {
        'cylinders': cylinders,
        'displacement': cylinders * np.random.uniform(25, 60, n_samples),
        'horsepower': cylinders * np.random.uniform(15, 35, n_samples),
        'weight': 1500 + cylinders * np.random.uniform(200, 500, n_samples) + np.random.normal(0, 200, n_samples),
        'acceleration': np.random.uniform(8, 24, n_samples),
        'model_year': np.random.randint(70, 83, n_samples),
        'origin': np.random.choice([1, 2, 3], n_samples, p=[0.5, 0.3, 0.2]),
    }
    
    df = pd.DataFrame(data)
    
    # Calculate MPG based on realistic relationships
    # Inverse relationships: higher weight, displacement, horsepower = lower MPG
    # Positive relationships: newer year, fewer cylinders = higher MPG
    base_mpg = 30
    
    mpg = base_mpg + (
        -df['weight'] / 200 +
        -df['displacement'] / 15 +
        -df['horsepower'] / 8 +
        df['model_year'] * 0.3 +
        (df['origin'] == 3) * 5 +  # Japanese cars more efficient
        (df['cylinders'] == 4) * 5 +
        df['acceleration'] * 0.2 +
        np.random.normal(0, 2, n_samples)
    )
    
    df['mpg'] = np.clip(mpg, 9, 47)
    df['car_name'] = [f'Car_{i}' for i in range(n_samples)]
    
    print(f"[+] Synthetic dataset created!")
    print(f"[+] MPG range: {df['mpg'].min():.1f} - {df['mpg'].max():.1f}")
    
    return df

def preprocess_auto_mpg(df):
    """
    Preprocess Auto MPG dataset
    
    Args:
        df (pd.DataFrame): Raw auto data
        
    Returns:
        pd.DataFrame: Preprocessed data
    """
    print("\n[+] Preprocessing Auto MPG data...")
    
    df_processed = df.copy()
    
    # Handle missing values in horsepower
    if df_processed['horsepower'].isna().any():
        print(f"[+] Found {df_processed['horsepower'].isna().sum()} missing horsepower values")
        df_processed['horsepower'] = df_processed['horsepower'].fillna(df_processed['horsepower'].median())
    
    # Convert horsepower to numeric if it's not
    df_processed['horsepower'] = pd.to_numeric(df_processed['horsepower'], errors='coerce')
    
    # Create origin categories (1=USA, 2=Europe, 3=Japan)
    df_processed['origin_usa'] = (df_processed['origin'] == 1).astype(int)
    df_processed['origin_europe'] = (df_processed['origin'] == 2).astype(int)
    df_processed['origin_japan'] = (df_processed['origin'] == 3).astype(int)
    
    # Create cylinder categories
    df_processed['cyl_4'] = (df_processed['cylinders'] == 4).astype(int)
    df_processed['cyl_6'] = (df_processed['cylinders'] == 6).astype(int)
    df_processed['cyl_8'] = (df_processed['cylinders'] == 8).astype(int)
    
    # Create derived features
    df_processed['power_to_weight'] = df_processed['horsepower'] / df_processed['weight']
    df_processed['displacement_per_cyl'] = df_processed['displacement'] / df_processed['cylinders']
    
    # Drop car name and original categorical columns for modeling
    columns_to_drop = ['car_name', 'origin']
    df_processed = df_processed.drop(columns=columns_to_drop, errors='ignore')
    
    print(f"[+] Preprocessing complete!")
    print(f"[+] Final shape: {df_processed.shape}")
    
    return df_processed

def prepare_features_target(df, target_col='mpg'):
    """
    Separate features and target variable
    
    Args:
        df (pd.DataFrame): Preprocessed data
        target_col (str): Name of target column
        
    Returns:
        pd.DataFrame: Feature matrix X
        pd.Series: Target vector y
    """
    print(f"\n[+] Preparing features and target...")
    
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found")
    
    y = df[target_col]
    X = df.drop(columns=[target_col])
    
    print(f"[+] Features shape: {X.shape}")
    print(f"[+] Target shape: {y.shape}")
    print(f"[+] Feature columns: {list(X.columns)}")
    
    return X, y
