"""
Data loading utilities for Unemployment Rates Dataset
"""
import pandas as pd
import numpy as np

def load_unemployment_data():
    """Load World Bank Economic Indicators / Unemployment Dataset"""
    print("[+] Loading Unemployment Rates Dataset...")
    
    try:
        # Try multiple sources
        sources = [
            "https://raw.githubusercontent.com/datasets/employment-us/master/data/employment-us.csv",
            "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Unemployment%20rate%20%E2%80%93%20World%20Bank/Unemployment%20rate%20%E2%80%93%20World%20Bank.csv"
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
        print(f"[+] Creating synthetic unemployment dataset...")
        return create_synthetic_unemployment()

def create_synthetic_unemployment(n_samples=500):
    """Create synthetic unemployment dataset"""
    np.random.seed(42)
    
    print(f"[+] Generating synthetic dataset with {n_samples} country-year observations...")
    
    # Generate economic indicators with more variance
    data = {
        'year': np.random.randint(2000, 2024, n_samples),
        'gdp_growth': np.random.normal(2.5, 4.0, n_samples),  # % GDP growth (increased variance)
        'inflation_rate': np.random.normal(3.0, 3.5, n_samples),  # % inflation (increased variance)
        'interest_rate': np.random.uniform(0, 10, n_samples),  # % interest rate
        'education_index': np.random.uniform(0.3, 0.95, n_samples),  # 0-1 scale (wider range)
        'population_growth': np.random.normal(1.0, 1.2, n_samples),  # % (increased variance)
        'labor_force_participation': np.random.uniform(45, 85, n_samples),  # % (wider range)
        'urban_population': np.random.uniform(30, 98, n_samples),  # % (wider range)
        'technology_index': np.random.uniform(0.2, 0.95, n_samples),  # 0-1 scale (wider range)
        'trade_openness': np.random.uniform(15, 180, n_samples),  # % of GDP (wider range)
        'government_spending': np.random.uniform(12, 55, n_samples),  # % of GDP (wider range)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate unemployment rate based on economic theory (stronger relationships)
    unemployment = (
        12.0 +  # Base unemployment
        -1.2 * df['gdp_growth'] +  # Okun's Law (stronger negative relationship)
        0.8 * df['inflation_rate'] +  # Phillips Curve
        0.5 * df['interest_rate'] +  # High rates reduce employment
        -15.0 * df['education_index'] +  # Education reduces unemployment (stronger)
        0.8 * df['population_growth'] +  # Population growth increases unemployment
        -0.12 * df['labor_force_participation'] +  # Participation effect
        -0.08 * df['urban_population'] +  # Urbanization effect
        -6.0 * df['technology_index'] +  # Technology adoption
        -0.03 * df['trade_openness'] +  # Trade openness effect
        0.12 * df['government_spending'] +  # Government spending
        np.random.normal(0, 2.5, n_samples)  # Random variation
    )
    
    df['unemployment_rate'] = np.clip(unemployment, 2, 25)
    
    print(f"[+] Dataset created! Unemployment: {df['unemployment_rate'].min():.2f}% - {df['unemployment_rate'].max():.2f}%")
    print(f"[+] Average unemployment: {df['unemployment_rate'].mean():.2f}%")
    return df

def preprocess_unemployment_data(df):
    """Preprocess unemployment dataset"""
    print("\n[+] Preprocessing unemployment data...")
    
    df_processed = df.copy()
    
    # Create GDP growth categories
    if 'gdp_growth' in df_processed.columns:
        df_processed['gdp_recession'] = (df_processed['gdp_growth'] < 0).astype(int)
        df_processed['gdp_slow'] = ((df_processed['gdp_growth'] >= 0) & (df_processed['gdp_growth'] < 2)).astype(int)
        df_processed['gdp_moderate'] = ((df_processed['gdp_growth'] >= 2) & (df_processed['gdp_growth'] < 4)).astype(int)
        df_processed['gdp_strong'] = (df_processed['gdp_growth'] >= 4).astype(int)
    
    # Create inflation categories
    if 'inflation_rate' in df_processed.columns:
        df_processed['inflation_low'] = (df_processed['inflation_rate'] < 2).astype(int)
        df_processed['inflation_target'] = ((df_processed['inflation_rate'] >= 2) & (df_processed['inflation_rate'] < 4)).astype(int)
        df_processed['inflation_high'] = (df_processed['inflation_rate'] >= 4).astype(int)
    
    # Create education level categories
    if 'education_index' in df_processed.columns:
        df_processed['education_low'] = (df_processed['education_index'] < 0.6).astype(int)
        df_processed['education_medium'] = ((df_processed['education_index'] >= 0.6) & (df_processed['education_index'] < 0.8)).astype(int)
        df_processed['education_high'] = (df_processed['education_index'] >= 0.8).astype(int)
    
    # Interaction features
    if 'gdp_growth' in df_processed.columns and 'inflation_rate' in df_processed.columns:
        df_processed['gdp_x_inflation'] = df_processed['gdp_growth'] * df_processed['inflation_rate']
    
    if 'education_index' in df_processed.columns and 'technology_index' in df_processed.columns:
        df_processed['education_x_tech'] = df_processed['education_index'] * df_processed['technology_index']
    
    if 'labor_force_participation' in df_processed.columns and 'urban_population' in df_processed.columns:
        df_processed['labor_x_urban'] = df_processed['labor_force_participation'] * df_processed['urban_population'] / 100
    
    # Time-based features if year exists
    if 'year' in df_processed.columns:
        df_processed['year_normalized'] = (df_processed['year'] - 2000) / 24  # Normalize to 0-1
        df_processed['post_2008_crisis'] = (df_processed['year'] >= 2008).astype(int)
        df_processed['post_2020_pandemic'] = (df_processed['year'] >= 2020).astype(int)
    
    print(f"[+] Preprocessing complete! Shape: {df_processed.shape}")
    return df_processed

def prepare_features_target(df, target_col='unemployment_rate'):
    """Separate features and target"""
    print(f"\n[+] Preparing features and target...")
    
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found")
    
    y = df[target_col]
    X = df.drop(columns=[target_col])
    
    print(f"[+] Features: {X.shape} | Target: {y.shape}")
    return X, y
