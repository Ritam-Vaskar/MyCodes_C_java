"""
Data loading utilities for Student Performance Dataset
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def create_synthetic_student_data(n_samples=400):
    """
    Create synthetic student performance dataset for demonstration
    
    Args:
        n_samples (int): Number of students to generate
        
    Returns:
        pd.DataFrame: Synthetic student data
    """
    np.random.seed(42)
    
    print(f"[+] Generating synthetic dataset with {n_samples} students...")
    
    data = {
        # Demographic
        'school': np.random.choice(['GP', 'MS'], n_samples, p=[0.7, 0.3]),
        'sex': np.random.choice(['F', 'M'], n_samples, p=[0.5, 0.5]),
        'age': np.random.randint(15, 23, n_samples),
        'address': np.random.choice(['U', 'R'], n_samples, p=[0.65, 0.35]),
        'famsize': np.random.choice(['GT3', 'LE3'], n_samples, p=[0.6, 0.4]),
        'Pstatus': np.random.choice(['T', 'A'], n_samples, p=[0.85, 0.15]),
        
        # Family background
        'Medu': np.random.randint(0, 5, n_samples),
        'Fedu': np.random.randint(0, 5, n_samples),
        'Mjob': np.random.choice(['teacher', 'health', 'services', 'at_home', 'other'], n_samples),
        'Fjob': np.random.choice(['teacher', 'health', 'services', 'at_home', 'other'], n_samples),
        'reason': np.random.choice(['home', 'reputation', 'course', 'other'], n_samples),
        'guardian': np.random.choice(['mother', 'father', 'other'], n_samples, p=[0.6, 0.3, 0.1]),
        
        # Academic
        'traveltime': np.random.randint(1, 5, n_samples),
        'studytime': np.random.randint(1, 5, n_samples),
        'failures': np.random.choice([0, 1, 2, 3], n_samples, p=[0.6, 0.25, 0.1, 0.05]),
        'schoolsup': np.random.choice(['yes', 'no'], n_samples, p=[0.3, 0.7]),
        'famsup': np.random.choice(['yes', 'no'], n_samples, p=[0.6, 0.4]),
        'paid': np.random.choice(['yes', 'no'], n_samples, p=[0.4, 0.6]),
        'activities': np.random.choice(['yes', 'no'], n_samples, p=[0.5, 0.5]),
        'nursery': np.random.choice(['yes', 'no'], n_samples, p=[0.7, 0.3]),
        'higher': np.random.choice(['yes', 'no'], n_samples, p=[0.9, 0.1]),
        'internet': np.random.choice(['yes', 'no'], n_samples, p=[0.7, 0.3]),
        'romantic': np.random.choice(['yes', 'no'], n_samples, p=[0.4, 0.6]),
        
        # Behavioral
        'famrel': np.random.randint(1, 6, n_samples),
        'freetime': np.random.randint(1, 6, n_samples),
        'goout': np.random.randint(1, 6, n_samples),
        'Dalc': np.random.randint(1, 6, n_samples),
        'Walc': np.random.randint(1, 6, n_samples),
        'health': np.random.randint(1, 6, n_samples),
        'absences': np.random.randint(0, 40, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Generate realistic grades based on features
    # Base grade starts at 10
    base_grade = 10
    
    # Positive influences
    grade_effect = (
        df['studytime'] * 1.5 +  # Study time helps
        df['Medu'] * 0.8 +  # Mother's education
        df['Fedu'] * 0.8 +  # Father's education
        (df['higher'] == 'yes') * 2 +  # Wants higher education
        (df['schoolsup'] == 'yes') * 1 +  # School support
        (df['famsup'] == 'yes') * 1 +  # Family support
        (df['internet'] == 'yes') * 1.5  # Internet access
    )
    
    # Negative influences
    grade_effect -= (
        df['failures'] * 3 +  # Past failures hurt
        df['goout'] * 0.5 +  # Going out too much
        df['Walc'] * 0.8 +  # Weekend alcohol
        df['Dalc'] * 0.8 +  # Daily alcohol
        df['absences'] * 0.1  # Absences
    )
    
    # Calculate grades with some randomness
    df['G1'] = np.clip(base_grade + grade_effect * 0.3 + np.random.normal(0, 1.5, n_samples), 0, 20)
    df['G2'] = np.clip(df['G1'] + np.random.normal(0, 1, n_samples), 0, 20)
    df['G3'] = np.clip(df['G2'] + np.random.normal(0, 1, n_samples), 0, 20)
    
    # Round grades to 1 decimal
    df['G1'] = df['G1'].round(1)
    df['G2'] = df['G2'].round(1)
    df['G3'] = df['G3'].round(1)
    
    print(f"[+] Synthetic dataset created successfully!")
    print(f"[+] Grade range: {df['G3'].min():.1f} - {df['G3'].max():.1f}")
    print(f"[+] Average grade: {df['G3'].mean():.2f}")
    
    return df

def load_student_data():
    """
    Load the Student Performance Dataset from UCI ML Repository
    
    Returns:
        pd.DataFrame: Loaded and preprocessed student performance data
    """
    print("[+] Attempting to load Student Performance Dataset...")
    
    # Try multiple sources for the student performance dataset
    sources = [
        {
            'url': "https://raw.githubusercontent.com/arunkumarpro1/student-performance-prediction/master/student-mat.csv",
            'sep': ';',
            'name': 'GitHub - Student Math Performance'
        },
        {
            'url': "https://raw.githubusercontent.com/uciml/student-performance/master/student-mat.csv",
            'sep': ';',
            'name': 'GitHub - UCI Repository'
        },
        {
            'url': "https://raw.githubusercontent.com/srivatsan88/End-to-End-ML-Project/master/data/student-mat.csv",
            'sep': ';',
            'name': 'GitHub - Alternative 1'
        }
    ]
    
    # Try each source
    for source in sources:
        try:
            print(f"[+] Trying source: {source['name']}...")
            df = pd.read_csv(source['url'], sep=source['sep'])
            
            print(f"[+] Dataset loaded successfully!")
            print(f"[+] Shape: {df.shape}")
            print(f"[+] Columns: {list(df.columns)}")
            
            # Verify it has the expected structure
            if 'G3' in df.columns or any('grade' in col.lower() for col in df.columns):
                return df
            else:
                print(f"[!] Dataset doesn't have expected grade columns, trying next source...")
                continue
                
        except Exception as e:
            print(f"[!] Failed to load from {source['name']}: {e}")
            continue
    
    # If all sources fail, create a synthetic dataset for demonstration
    print(f"[!] All online sources failed. Creating synthetic dataset for demonstration...")
    return create_synthetic_student_data()

def preprocess_student_data(df):
    """
    Preprocess student performance data
    - Handle categorical variables
    - Create derived features
    - Clean missing values
    
    Args:
        df (pd.DataFrame): Raw student data
        
    Returns:
        pd.DataFrame: Preprocessed data
        dict: Encoding mappings
    """
    print("\n[+] Preprocessing student data...")
    
    # Create a copy to avoid modifying original
    df_processed = df.copy()
    
    # Initialize label encoders dictionary
    encoders = {}
    
    # Encode binary categorical variables
    binary_cols = {
        'school': {'GP': 1, 'MS': 0},
        'sex': {'F': 0, 'M': 1},
        'address': {'U': 1, 'R': 0},
        'famsize': {'GT3': 1, 'LE3': 0},
        'Pstatus': {'T': 1, 'A': 0},
        'schoolsup': {'yes': 1, 'no': 0},
        'famsup': {'yes': 1, 'no': 0},
        'paid': {'yes': 1, 'no': 0},
        'activities': {'yes': 1, 'no': 0},
        'nursery': {'yes': 1, 'no': 0},
        'higher': {'yes': 1, 'no': 0},
        'internet': {'yes': 1, 'no': 0},
        'romantic': {'yes': 1, 'no': 0}
    }
    
    for col, mapping in binary_cols.items():
        if col in df_processed.columns:
            df_processed[col] = df_processed[col].map(mapping)
            encoders[col] = mapping
    
    # Encode ordinal categorical variables
    ordinal_cols = {
        'Medu': None,  # Already numeric (0-4)
        'Fedu': None,  # Already numeric (0-4)
        'Mjob': None,  # Will be label encoded
        'Fjob': None,  # Will be label encoded
        'reason': None,  # Will be label encoded
        'guardian': None  # Will be label encoded
    }
    
    # Label encode nominal categorical variables
    nominal_cols = ['Mjob', 'Fjob', 'reason', 'guardian']
    
    for col in nominal_cols:
        if col in df_processed.columns:
            le = LabelEncoder()
            df_processed[col] = le.fit_transform(df_processed[col])
            encoders[col] = dict(zip(le.classes_, le.transform(le.classes_)))
    
    # Create derived features
    if 'studytime' in df_processed.columns and 'failures' in df_processed.columns:
        # Study efficiency score
        df_processed['study_efficiency'] = df_processed['studytime'] / (df_processed['failures'] + 1)
    
    if 'Medu' in df_processed.columns and 'Fedu' in df_processed.columns:
        # Average parental education
        df_processed['avg_parent_edu'] = (df_processed['Medu'] + df_processed['Fedu']) / 2
    
    if 'G1' in df_processed.columns and 'G2' in df_processed.columns:
        # Grade improvement trend
        df_processed['grade_trend'] = df_processed['G2'] - df_processed['G1']
    
    # Handle missing values
    df_processed = df_processed.fillna(df_processed.median(numeric_only=True))
    
    print(f"[+] Preprocessing complete!")
    print(f"[+] Processed shape: {df_processed.shape}")
    print(f"[+] Encoded {len(encoders)} categorical features")
    
    return df_processed, encoders

def prepare_features_target(df, target_col='G3'):
    """
    Separate features and target variable
    
    Args:
        df (pd.DataFrame): Preprocessed data
        target_col (str): Name of target column (default: 'G3' - final grade)
        
    Returns:
        pd.DataFrame: Feature matrix X
        pd.Series: Target vector y
    """
    print(f"\n[+] Preparing features and target...")
    
    # Ensure target column exists
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset")
    
    # Separate features and target
    y = df[target_col]
    
    # Drop target and intermediate grade columns for prediction
    cols_to_drop = [target_col]
    if target_col == 'G3':
        # If predicting final grade, also drop intermediate grades
        cols_to_drop.extend(['G1', 'G2'])
    
    X = df.drop(columns=cols_to_drop, errors='ignore')
    
    print(f"[+] Features shape: {X.shape}")
    print(f"[+] Target shape: {y.shape}")
    print(f"[+] Feature columns: {list(X.columns)}")
    
    return X, y

def get_feature_groups():
    """
    Get feature groups for analysis
    
    Returns:
        dict: Dictionary of feature groups
    """
    return {
        'demographic': ['age', 'sex', 'address', 'famsize', 'Pstatus'],
        'family_background': ['Medu', 'Fedu', 'Mjob', 'Fjob', 'guardian', 'avg_parent_edu'],
        'academic': ['school', 'studytime', 'failures', 'schoolsup', 'higher', 'study_efficiency'],
        'social': ['famsup', 'paid', 'activities', 'nursery', 'internet', 'romantic'],
        'behavioral': ['traveltime', 'goout', 'Dalc', 'Walc', 'health', 'absences']
    }
