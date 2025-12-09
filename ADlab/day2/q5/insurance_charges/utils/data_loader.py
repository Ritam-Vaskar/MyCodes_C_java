"""
Data loading utilities for Health Insurance Dataset
"""
import pandas as pd
import numpy as np

def load_insurance_data():
    """
    Load the Health Insurance Dataset
    
    Returns:
        pd.DataFrame: Loaded insurance data
    """
    print("[+] Loading Health Insurance Dataset...")
    
    try:
        # Try multiple sources
        sources = [
            "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv",
            "https://raw.githubusercontent.com/JovianML/opendatasets/master/data/medical-insurance-payout/insurance.csv"
        ]
        
        for url in sources:
            try:
                df = pd.read_csv(url)
                print(f"[+] Dataset loaded successfully!")
                print(f"[+] Shape: {df.shape}")
                print(f"[+] Columns: {list(df.columns)}")
                return df
            except:
                continue
        
        raise Exception("All sources failed")
        
    except Exception as e:
        print(f"[!] Error loading dataset: {e}")
        print(f"[+] Creating synthetic Health Insurance dataset...")
        return create_synthetic_insurance(n_samples=1338)

def create_synthetic_insurance(n_samples=1338):
    """
    Create synthetic health insurance dataset
    
    Args:
        n_samples (int): Number of people to generate
        
    Returns:
        pd.DataFrame: Synthetic insurance data
    """
    np.random.seed(42)
    
    print(f"[+] Generating synthetic dataset with {n_samples} people...")
    
    data = {
        'age': np.random.randint(18, 65, n_samples),
        'sex': np.random.choice(['male', 'female'], n_samples),
        'bmi': np.random.normal(30, 6, n_samples),
        'children': np.random.choice([0, 1, 2, 3, 4, 5], n_samples, p=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03]),
        'smoker': np.random.choice(['yes', 'no'], n_samples, p=[0.2, 0.8]),
        'region': np.random.choice(['northeast', 'northwest', 'southeast', 'southwest'], n_samples)
    }
    
    df = pd.DataFrame(data)
    df['bmi'] = np.clip(df['bmi'], 15, 53)
    
    # Calculate charges based on realistic relationships
    base_charge = 5000
    
    charges = base_charge + (
        df['age'] * 250 +
        (df['bmi'] - 25) * 100 +
        df['children'] * 500 +
        (df['smoker'] == 'yes') * 23000 +  # Smoking has huge impact
        (df['sex'] == 'male') * 500 +
        np.random.normal(0, 2000, n_samples)
    )
    
    df['charges'] = np.clip(charges, 1000, 65000)
    
    print(f"[+] Synthetic dataset created!")
    print(f"[+] Charges range: ${df['charges'].min():.2f} - ${df['charges'].max():.2f}")
    
    return df

def preprocess_insurance_data(df):
    """
    Preprocess health insurance dataset
    
    Args:
        df (pd.DataFrame): Raw insurance data
        
    Returns:
        pd.DataFrame: Preprocessed data
    """
    print("\n[+] Preprocessing Insurance data...")
    
    df_processed = df.copy()
    
    # Encode binary variables
    df_processed['sex_male'] = (df_processed['sex'] == 'male').astype(int)
    df_processed['smoker_yes'] = (df_processed['smoker'] == 'yes').astype(int)
    
    # One-hot encode region
    df_processed['region_northeast'] = (df_processed['region'] == 'northeast').astype(int)
    df_processed['region_northwest'] = (df_processed['region'] == 'northwest').astype(int)
    df_processed['region_southeast'] = (df_processed['region'] == 'southeast').astype(int)
    df_processed['region_southwest'] = (df_processed['region'] == 'southwest').astype(int)
    
    # Create BMI categories
    df_processed['bmi_category'] = pd.cut(
        df_processed['bmi'], 
        bins=[0, 18.5, 25, 30, 100],
        labels=[0, 1, 2, 3]  # Underweight, Normal, Overweight, Obese
    ).astype(int)
    
    # Create age groups
    df_processed['age_group'] = pd.cut(
        df_processed['age'],
        bins=[0, 30, 45, 60, 100],
        labels=[0, 1, 2, 3]  # Young, Middle-aged, Senior, Elderly
    ).astype(int)
    
    # Interaction features
    df_processed['smoker_bmi'] = df_processed['smoker_yes'] * df_processed['bmi']
    df_processed['age_bmi'] = df_processed['age'] * df_processed['bmi']
    
    # Drop original categorical columns
    df_processed = df_processed.drop(columns=['sex', 'smoker', 'region'], errors='ignore')
    
    print(f"[+] Preprocessing complete!")
    print(f"[+] Final shape: {df_processed.shape}")
    
    return df_processed

def prepare_features_target(df, target_col='charges'):
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
