"""
Data Preprocessing and Visualization Demo
==========================================
This program demonstrates:
1. Handling missing values
2. Encoding categorical data
3. Feature scaling
4. Data visualization with matplotlib and seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

class DataPreprocessor:
    """Class to handle data preprocessing operations"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def create_sample_dataset(self):
        """Create a sample dataset with missing values and categorical data"""
        print("=" * 60)
        print("CREATING SAMPLE DATASET")
        print("=" * 60)
        
        np.random.seed(42)
        n_samples = 150
        
        data = {
            'sepal_length': np.random.normal(5.8, 0.8, n_samples),
            'sepal_width': np.random.normal(3.0, 0.4, n_samples),
            'petal_length': np.random.normal(3.8, 1.8, n_samples),
            'petal_width': np.random.normal(1.2, 0.8, n_samples),
            'species': np.random.choice(['setosa', 'versicolor', 'virginica'], n_samples),
            'quality': np.random.choice(['Low', 'Medium', 'High'], n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Introduce some missing values
        missing_indices = np.random.choice(df.index, size=15, replace=False)
        df.loc[missing_indices[:5], 'sepal_length'] = np.nan
        df.loc[missing_indices[5:10], 'petal_length'] = np.nan
        df.loc[missing_indices[10:15], 'sepal_width'] = np.nan
        
        print(f"\nDataset created with {len(df)} samples")
        print(f"Features: {list(df.columns)}")
        print(f"\nFirst 5 rows:")
        print(df.head())
        print(f"\nDataset Info:")
        print(df.info())
        
        return df
    
    def handle_missing_values(self, df):
        """Handle missing values using mean imputation"""
        print("\n" + "=" * 60)
        print("HANDLING MISSING VALUES")
        print("=" * 60)
        
        print("\nMissing values before handling:")
        print(df.isnull().sum())
        
        # Separate numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Use mean imputation for numeric columns
        imputer = SimpleImputer(strategy='mean')
        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
        
        print("\nMissing values after handling:")
        print(df.isnull().sum())
        print("\n✓ Missing values handled using mean imputation")
        
        return df
    
    def encode_categorical_data(self, df):
        """Encode categorical data using Label Encoding"""
        print("\n" + "=" * 60)
        print("ENCODING CATEGORICAL DATA")
        print("=" * 60)
        
        categorical_cols = df.select_dtypes(include=['object']).columns
        print(f"\nCategorical columns found: {list(categorical_cols)}")
        
        df_encoded = df.copy()
        
        for col in categorical_cols:
            le = LabelEncoder()
            df_encoded[f'{col}_encoded'] = le.fit_transform(df[col])
            self.label_encoders[col] = le
            
            print(f"\n{col}:")
            print(f"  Original values: {df[col].unique()}")
            print(f"  Encoded values: {df_encoded[f'{col}_encoded'].unique()}")
            print(f"  Mapping: {dict(zip(le.classes_, le.transform(le.classes_)))}")
        
        print("\n✓ Categorical data encoded successfully")
        return df_encoded
    
    def feature_scaling(self, df):
        """Apply feature scaling using StandardScaler"""
        print("\n" + "=" * 60)
        print("FEATURE SCALING")
        print("=" * 60)
        
        # Select numeric columns (excluding encoded categorical)
        numeric_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        
        print("\nOriginal data statistics:")
        print(df[numeric_cols].describe())
        
        # Scale features
        df_scaled = df.copy()
        df_scaled[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
        
        print("\nScaled data statistics:")
        print(df_scaled[numeric_cols].describe())
        print("\n✓ Features scaled using StandardScaler (mean=0, std=1)")
        
        return df_scaled
    
    def visualize_distributions(self, df, df_scaled):
        """Plot distributions of features"""
        print("\n" + "=" * 60)
        print("VISUALIZING FEATURE DISTRIBUTIONS")
        print("=" * 60)
        
        numeric_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        fig.suptitle('Feature Distributions: Original vs Scaled', fontsize=16, fontweight='bold')
        
        for idx, col in enumerate(numeric_cols):
            # Original distribution
            axes[0, idx].hist(df[col], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
            axes[0, idx].set_title(f'Original {col}', fontsize=10)
            axes[0, idx].set_xlabel('Value')
            axes[0, idx].set_ylabel('Frequency')
            axes[0, idx].grid(True, alpha=0.3)
            
            # Scaled distribution
            axes[1, idx].hist(df_scaled[col], bins=20, color='lightcoral', edgecolor='black', alpha=0.7)
            axes[1, idx].set_title(f'Scaled {col}', fontsize=10)
            axes[1, idx].set_xlabel('Value')
            axes[1, idx].set_ylabel('Frequency')
            axes[1, idx].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('c:\\C programing\\ADlab\\data_preprocessing\\output\\distribution_plots.png', dpi=300, bbox_inches='tight')
        print("\n✓ Distribution plots saved as 'distribution_plots.png'")
        plt.show()
    
    def visualize_scatter_plots(self, df):
        """Create scatter plots to understand relationships between features"""
        print("\n" + "=" * 60)
        print("CREATING SCATTER PLOTS")
        print("=" * 60)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        fig.suptitle('Feature Relationships (Scatter Plots)', fontsize=16, fontweight='bold')
        
        # Scatter plot 1: Sepal Length vs Sepal Width
        sns.scatterplot(data=df, x='sepal_length', y='sepal_width', 
                       hue='species', style='species', s=100, ax=axes[0, 0])
        axes[0, 0].set_title('Sepal Length vs Sepal Width', fontsize=12)
        axes[0, 0].grid(True, alpha=0.3)
        
        # Scatter plot 2: Petal Length vs Petal Width
        sns.scatterplot(data=df, x='petal_length', y='petal_width', 
                       hue='species', style='species', s=100, ax=axes[0, 1])
        axes[0, 1].set_title('Petal Length vs Petal Width', fontsize=12)
        axes[0, 1].grid(True, alpha=0.3)
        
        # Scatter plot 3: Sepal Length vs Petal Length
        sns.scatterplot(data=df, x='sepal_length', y='petal_length', 
                       hue='quality', style='quality', s=100, ax=axes[1, 0])
        axes[1, 0].set_title('Sepal Length vs Petal Length', fontsize=12)
        axes[1, 0].grid(True, alpha=0.3)
        
        # Scatter plot 4: Sepal Width vs Petal Width
        sns.scatterplot(data=df, x='sepal_width', y='petal_width', 
                       hue='quality', style='quality', s=100, ax=axes[1, 1])
        axes[1, 1].set_title('Sepal Width vs Petal Width', fontsize=12)
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('c:\\C programing\\ADlab\\data_preprocessing\\output\\scatter_plots.png', dpi=300, bbox_inches='tight')
        print("\n✓ Scatter plots saved as 'scatter_plots.png'")
        plt.show()
    
    def visualize_correlation_heatmap(self, df):
        """Create correlation heatmap"""
        print("\n" + "=" * 60)
        print("CREATING CORRELATION HEATMAP")
        print("=" * 60)
        
        # Select numeric columns for correlation
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlation_matrix = df[numeric_cols].corr()
        
        print("\nCorrelation Matrix:")
        print(correlation_matrix)
        
        # Create heatmap
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title('Correlation Heatmap - Feature Relationships', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('c:\\C programing\\ADlab\\data_preprocessing\\output\\correlation_heatmap.png', dpi=300, bbox_inches='tight')
        print("\n✓ Correlation heatmap saved as 'correlation_heatmap.png'")
        plt.show()
        
        # Print strong correlations
        print("\nStrong Correlations (|r| > 0.5):")
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                if abs(correlation_matrix.iloc[i, j]) > 0.5:
                    print(f"  {correlation_matrix.columns[i]} <-> {correlation_matrix.columns[j]}: "
                          f"{correlation_matrix.iloc[i, j]:.3f}")
    
    def save_processed_data(self, df_original, df_processed):
        """Save both original and processed datasets"""
        print("\n" + "=" * 60)
        print("SAVING PROCESSED DATA")
        print("=" * 60)
        
        df_original.to_csv('c:\\C programing\\ADlab\\data_preprocessing\\output\\original_data.csv', index=False)
        df_processed.to_csv('c:\\C programing\\ADlab\\data_preprocessing\\output\\processed_data.csv', index=False)
        
        print("\n✓ Original data saved as 'original_data.csv'")
        print("✓ Processed data saved as 'processed_data.csv'")


def main():
    """Main function to run the data preprocessing pipeline"""
    print("\n" + "=" * 60)
    print("DATA PREPROCESSING AND VISUALIZATION PIPELINE")
    print("=" * 60)
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Step 1: Create sample dataset
    df = preprocessor.create_sample_dataset()
    df_original = df.copy()
    
    # Step 2: Handle missing values
    df = preprocessor.handle_missing_values(df)
    
    # Step 3: Encode categorical data
    df_encoded = preprocessor.encode_categorical_data(df)
    
    # Step 4: Feature scaling
    df_scaled = preprocessor.feature_scaling(df_encoded)
    
    # Step 5: Visualizations
    preprocessor.visualize_distributions(df, df_scaled)
    preprocessor.visualize_scatter_plots(df)
    preprocessor.visualize_correlation_heatmap(df_encoded)
    
    # Step 6: Save processed data
    preprocessor.save_processed_data(df_original, df_encoded)
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nAll visualizations have been saved in the 'output' folder:")
    print("  - distribution_plots.png")
    print("  - scatter_plots.png")
    print("  - correlation_heatmap.png")
    print("  - original_data.csv")
    print("  - processed_data.csv")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
