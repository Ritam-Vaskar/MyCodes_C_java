"""
Data Loading Utilities for Time Series Dataset
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta


def load_data():
    """
    Load Weather/Temperature Time Series Dataset
    Returns: df (DataFrame with date and temperature)
    """
    print("Loading Time Series Dataset...")
    
    # Try loading from online source
    data_url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv"
    
    try:
        df = pd.read_csv(data_url)
        df.columns = ['Date', 'Temperature']
        df['Date'] = pd.to_datetime(df['Date'])
        
        print("Dataset loaded successfully!")
        print(f"Shape: {df.shape}")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"Total days: {len(df)}")
        
        return df
    
    except Exception as e:
        print(f"Error loading from online source: {e}")
        print("\nCreating sample time series dataset...")
        
        # Create sample time series data
        np.random.seed(42)
        days = 365 * 3  # 3 years of data
        
        start_date = datetime(2020, 1, 1)
        dates = [start_date + timedelta(days=i) for i in range(days)]
        
        # Generate temperature with trend and seasonality
        t = np.arange(days)
        trend = 0.01 * t  # Slight upward trend
        seasonal = 10 * np.sin(2 * np.pi * t / 365)  # Annual seasonality
        noise = np.random.normal(0, 2, days)
        temperature = 15 + trend + seasonal + noise
        
        df = pd.DataFrame({
            'Date': dates,
            'Temperature': temperature
        })
        
        print("Sample dataset created successfully!")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        
        return df


def prepare_time_series_features(df):
    """
    Prepare features for time series forecasting
    """
    df = df.copy()
    
    # Add time-based features
    df['DayOfYear'] = df['Date'].dt.dayofyear
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    
    # Add cyclical features for seasonality
    df['Sin_DayOfYear'] = np.sin(2 * np.pi * df['DayOfYear'] / 365.25)
    df['Cos_DayOfYear'] = np.cos(2 * np.pi * df['DayOfYear'] / 365.25)
    
    # Time index (days since start)
    df['TimeIndex'] = (df['Date'] - df['Date'].min()).dt.days
    
    print("\n" + "="*60)
    print("TIME SERIES FEATURES CREATED")
    print("="*60)
    print("Features added:")
    print("  - TimeIndex (linear trend)")
    print("  - DayOfYear, Month, Year")
    print("  - Sin_DayOfYear, Cos_DayOfYear (seasonality)")
    print("="*60)
    
    return df


def split_time_series_data(df, test_size=0.2):
    """
    Split time series data (chronological split)
    """
    split_idx = int(len(df) * (1 - test_size))
    
    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy()
    
    print(f"\nTime series split:")
    print(f"Training period: {train_df['Date'].min()} to {train_df['Date'].max()}")
    print(f"Testing period: {test_df['Date'].min()} to {test_df['Date'].max()}")
    print(f"Training samples: {len(train_df)}")
    print(f"Testing samples: {len(test_df)}")
    
    return train_df, test_df


def get_data_statistics(df):
    """
    Get descriptive statistics of the time series
    """
    print("\n" + "="*60)
    print("TIME SERIES STATISTICS")
    print("="*60)
    
    print(f"\nTemperature Statistics:")
    print(f"Mean: {df['Temperature'].mean():.2f}°")
    print(f"Median: {df['Temperature'].median():.2f}°")
    print(f"Min: {df['Temperature'].min():.2f}°")
    print(f"Max: {df['Temperature'].max():.2f}°")
    print(f"Std deviation: {df['Temperature'].std():.2f}°")
    
    print(f"\nData Quality:")
    print(f"Missing values: {df['Temperature'].isnull().sum()}")
    print(f"Total observations: {len(df)}")
    
    return df['Temperature'].describe()


def detect_trend(df):
    """
    Detect trend in time series
    """
    from scipy import stats
    
    x = np.arange(len(df))
    y = df['Temperature'].values
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    print("\n" + "="*60)
    print("TREND ANALYSIS")
    print("="*60)
    print(f"Linear trend slope: {slope:.6f}° per day")
    print(f"Correlation (r): {r_value:.4f}")
    print(f"R-squared: {r_value**2:.4f}")
    
    if abs(slope) < 0.001:
        trend_type = "No significant trend"
    elif slope > 0:
        trend_type = "Upward trend (warming)"
    else:
        trend_type = "Downward trend (cooling)"
    
    print(f"Trend type: {trend_type}")
    
    if p_value < 0.05:
        print(f"Trend is statistically significant (p < 0.05)")
    else:
        print(f"Trend is not statistically significant")
    
    return slope, intercept, r_value


def analyze_seasonality(df):
    """
    Analyze seasonal patterns
    """
    monthly_avg = df.groupby('Month')['Temperature'].mean()
    
    print("\n" + "="*60)
    print("SEASONALITY ANALYSIS")
    print("="*60)
    print("\nAverage Temperature by Month:")
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    for month, avg_temp in monthly_avg.items():
        print(f"  {months[month-1]}: {avg_temp:.2f}°")
    
    temp_range = monthly_avg.max() - monthly_avg.min()
    print(f"\nSeasonal temperature range: {temp_range:.2f}°")
    
    return monthly_avg
