# Data Preprocessing and Visualization Demo

This project demonstrates essential data preprocessing techniques and visualization methods in Python.

## Features

### 1. Data Preprocessing
- **Handling Missing Values**: Uses mean imputation to fill missing numeric values
- **Encoding Categorical Data**: Converts categorical variables to numeric using Label Encoding
- **Feature Scaling**: Standardizes features to have mean=0 and std=1 using StandardScaler

### 2. Data Visualization
- **Distribution Plots**: Histogram visualization of feature distributions (before and after scaling)
- **Scatter Plots**: Relationship analysis between features using Seaborn
- **Correlation Heatmap**: Visual representation of feature correlations

## Project Structure
```
data_preprocessing/
│
├── main.py                 # Main program file
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── output/                # Output directory for plots and processed data
    ├── distribution_plots.png
    ├── scatter_plots.png
    ├── correlation_heatmap.png
    ├── original_data.csv
    └── processed_data.csv
```

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the main program:
```bash
python main.py
```

## Output

The program will:
1. Create a sample dataset with missing values and categorical data
2. Display preprocessing steps in the console
3. Generate visualization plots (saved in `output/` folder)
4. Save processed datasets as CSV files

## Technologies Used

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Basic plotting
- **seaborn**: Advanced statistical visualizations
- **scikit-learn**: Machine learning preprocessing tools

## Author

Created as a demonstration of data preprocessing techniques for machine learning.
