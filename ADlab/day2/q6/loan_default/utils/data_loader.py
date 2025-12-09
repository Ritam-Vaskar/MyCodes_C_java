"""
Data loading utilities for Loan Default Dataset
"""
import pandas as pd
import numpy as np

def load_loan_default_data():
    """Load Loan Default Dataset"""
    print("[+] Loading Loan Default Dataset...")
    
    try:
        # Try Kaggle/GitHub sources
        sources = [
            "https://raw.githubusercontent.com/YBI-Foundation/Dataset/main/Loan%20Default.csv",
            "https://raw.githubusercontent.com/Dataweekends/zero_to_deep_learning_udemy/master/data/loan_data.csv"
        ]
        
        for url in sources:
            try:
                df = pd.read_csv(url)
                print(f"[+] Dataset loaded! Shape: {df.shape}")
                print(f"[+] Columns: {list(df.columns)}")
                return df
            except:
                continue
        
        raise Exception("All sources failed")
        
    except Exception as e:
        print(f"[!] Error: {e}")
        print(f"[+] Creating synthetic loan default dataset...")
        return create_synthetic_loan_default()

def create_synthetic_loan_default(n_samples=10000):
    """Create synthetic loan default dataset"""
    np.random.seed(42)
    
    print(f"[+] Generating synthetic dataset with {n_samples} loan applications...")
    
    # Generate features
    data = {
        'age': np.random.randint(18, 70, n_samples),
        'income': np.random.lognormal(10.5, 0.8, n_samples),  # $30k-$150k range
        'credit_score': np.clip(np.random.normal(680, 80, n_samples), 300, 850).astype(int),
        'loan_amount': np.random.uniform(5000, 50000, n_samples),
        'loan_term': np.random.choice([12, 24, 36, 48, 60], n_samples, p=[0.1, 0.2, 0.3, 0.25, 0.15]),
        'employment_length': np.random.randint(0, 30, n_samples),
        'home_ownership': np.random.choice(['RENT', 'OWN', 'MORTGAGE'], n_samples, p=[0.4, 0.2, 0.4]),
        'annual_inc': np.random.lognormal(10.8, 0.6, n_samples),
        'debt_to_income': np.random.uniform(0, 40, n_samples),
        'num_credit_lines': np.random.randint(1, 20, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate default probability and create target
    default_prob = (
        -0.05 * (df['credit_score'] - 680) / 80 +  # Credit score effect
        0.02 * (df['loan_amount'] - 25000) / 10000 +  # Loan amount effect
        0.015 * (df['loan_term'] - 36) / 12 +  # Loan term effect
        -0.03 * (df['income'] - 50000) / 20000 +  # Income effect (negative)
        0.02 * (df['debt_to_income'] - 20) / 10 +  # DTI effect
        np.random.normal(0, 0.05, n_samples)
    )
    
    # Convert to probability and binary default
    default_prob = 1 / (1 + np.exp(-default_prob))  # Sigmoid
    df['default'] = (default_prob > 0.5).astype(int)
    
    # Also add default_rate as continuous for regression
    df['default_rate'] = np.clip(default_prob * 100, 0, 100)
    
    print(f"[+] Dataset created! Default rate: {df['default'].mean()*100:.2f}%")
    return df

def preprocess_loan_data(df):
    """Preprocess loan default dataset"""
    print("\n[+] Preprocessing loan default data...")
    
    df_processed = df.copy()
    
    # Encode home ownership
    if 'home_ownership' in df_processed.columns:
        df_processed['home_rent'] = (df_processed['home_ownership'] == 'RENT').astype(int)
        df_processed['home_own'] = (df_processed['home_ownership'] == 'OWN').astype(int)
        df_processed['home_mortgage'] = (df_processed['home_ownership'] == 'MORTGAGE').astype(int)
        df_processed = df_processed.drop('home_ownership', axis=1)
    
    # Create risk categories
    if 'credit_score' in df_processed.columns:
        df_processed['credit_poor'] = (df_processed['credit_score'] < 600).astype(int)
        df_processed['credit_fair'] = ((df_processed['credit_score'] >= 600) & (df_processed['credit_score'] < 700)).astype(int)
        df_processed['credit_good'] = ((df_processed['credit_score'] >= 700) & (df_processed['credit_score'] < 750)).astype(int)
        df_processed['credit_excellent'] = (df_processed['credit_score'] >= 750).astype(int)
    
    # Create income brackets
    if 'income' in df_processed.columns:
        df_processed['income_low'] = (df_processed['income'] < 40000).astype(int)
        df_processed['income_medium'] = ((df_processed['income'] >= 40000) & (df_processed['income'] < 80000)).astype(int)
        df_processed['income_high'] = (df_processed['income'] >= 80000).astype(int)
    
    # Loan to income ratio
    if 'loan_amount' in df_processed.columns and 'income' in df_processed.columns:
        df_processed['loan_to_income'] = df_processed['loan_amount'] / (df_processed['income'] + 1)
    
    # Interaction features
    if 'credit_score' in df_processed.columns and 'loan_amount' in df_processed.columns:
        df_processed['credit_x_loan'] = df_processed['credit_score'] * df_processed['loan_amount'] / 10000
    
    if 'debt_to_income' in df_processed.columns and 'loan_term' in df_processed.columns:
        df_processed['dti_x_term'] = df_processed['debt_to_income'] * df_processed['loan_term']
    
    print(f"[+] Preprocessing complete! Shape: {df_processed.shape}")
    return df_processed

def prepare_features_target(df, target_col='default_rate'):
    """Separate features and target"""
    print(f"\n[+] Preparing features and target...")
    
    if target_col not in df.columns:
        # Try alternative target columns
        if 'default' in df.columns:
            target_col = 'default'
        elif 'default_rate' in df.columns:
            target_col = 'default_rate'
        else:
            raise ValueError(f"No suitable target column found")
    
    y = df[target_col]
    
    # Drop all potential target columns
    X = df.drop(columns=['default', 'default_rate'], errors='ignore')
    
    print(f"[+] Features: {X.shape} | Target: {y.shape}")
    print(f"[+] Target column: {target_col}")
    return X, y
