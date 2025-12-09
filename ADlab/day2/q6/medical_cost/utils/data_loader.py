"""
Data loading utilities for Medical Cost Personal Dataset
"""
import pandas as pd
import numpy as np

def load_medical_cost_data():
    """Load Medical Cost Personal Dataset from Kaggle/GitHub"""
    print("[+] Loading Medical Cost Personal Dataset...")
    
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
        print(f"[!] Error: {e}")
        print(f"[+] Creating synthetic medical cost dataset...")
        return create_synthetic_medical_cost()

def create_synthetic_medical_cost(n_samples=1338):
    """Create synthetic medical cost dataset"""
    np.random.seed(42)
    
    print(f"[+] Generating synthetic dataset with {n_samples} individuals...")
    
    data = {
        'age': np.random.randint(18, 65, n_samples),
        'sex': np.random.choice(['male', 'female'], n_samples),
        'bmi': np.clip(np.random.normal(30, 6, n_samples), 15, 53),
        'children': np.random.choice([0, 1, 2, 3, 4, 5], n_samples, p=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03]),
        'smoker': np.random.choice(['yes', 'no'], n_samples, p=[0.2, 0.8]),
        'region': np.random.choice(['northeast', 'northwest', 'southeast', 'southwest'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate charges
    base = 5000
    charges = base + (
        df['age'] * 250 +
        (df['bmi'] - 25) * 100 +
        df['children'] * 500 +
        (df['smoker'] == 'yes') * 23000 +
        (df['sex'] == 'male') * 500 +
        np.random.normal(0, 2000, n_samples)
    )
    
    df['charges'] = np.clip(charges, 1000, 65000)
    
    print(f"[+] Dataset created! Charges: ${df['charges'].min():.2f} - ${df['charges'].max():.2f}")
    return df

def preprocess_medical_data(df):
    """Preprocess medical cost dataset"""
    print("\n[+] Preprocessing medical cost data...")
    
    df_processed = df.copy()
    
    # Encode categorical variables
    df_processed['sex_male'] = (df_processed['sex'] == 'male').astype(int)
    df_processed['smoker_yes'] = (df_processed['smoker'] == 'yes').astype(int)
    
    # One-hot encode region
    for region in ['northeast', 'northwest', 'southeast', 'southwest']:
        df_processed[f'region_{region}'] = (df_processed['region'] == region).astype(int)
    
    # Create BMI categories
    df_processed['bmi_underweight'] = (df_processed['bmi'] < 18.5).astype(int)
    df_processed['bmi_normal'] = ((df_processed['bmi'] >= 18.5) & (df_processed['bmi'] < 25)).astype(int)
    df_processed['bmi_overweight'] = ((df_processed['bmi'] >= 25) & (df_processed['bmi'] < 30)).astype(int)
    df_processed['bmi_obese'] = (df_processed['bmi'] >= 30).astype(int)
    
    # Create age groups
    df_processed['age_young'] = (df_processed['age'] < 30).astype(int)
    df_processed['age_middle'] = ((df_processed['age'] >= 30) & (df_processed['age'] < 50)).astype(int)
    df_processed['age_senior'] = (df_processed['age'] >= 50).astype(int)
    
    # Interaction features
    df_processed['smoker_x_bmi'] = df_processed['smoker_yes'] * df_processed['bmi']
    df_processed['age_x_smoker'] = df_processed['age'] * df_processed['smoker_yes']
    df_processed['age_x_bmi'] = df_processed['age'] * df_processed['bmi']
    
    # Drop original categorical columns
    df_processed = df_processed.drop(columns=['sex', 'smoker', 'region'], errors='ignore')
    
    print(f"[+] Preprocessing complete! Shape: {df_processed.shape}")
    return df_processed

def prepare_features_target(df, target_col='charges'):
    """Separate features and target"""
    print(f"\n[+] Preparing features and target...")
    
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found")
    
    y = df[target_col]
    X = df.drop(columns=[target_col])
    
    print(f"[+] Features: {X.shape} | Target: {y.shape}")
    return X, y
