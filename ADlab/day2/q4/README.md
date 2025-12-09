# Student Performance Analysis Using Linear Regression

## Research Question
**How do factors such as study hours, attendance, socioeconomic background, and parental education impact academic performance?**

This project investigates the contribution of multiple factors to students' academic performance using Linear Regression analysis on the Student Performance Dataset from the UCI Machine Learning Repository.

---

## Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Key Features](#key-features)
- [Results](#results)
- [Insights](#insights)
- [Requirements](#requirements)

---

## Overview

Academic performance is influenced by a complex interplay of various factors including:
- **Study hours**: Time dedicated to studying
- **Attendance**: Class participation and regularity
- **Socioeconomic background**: Family economic status and home environment
- **Parental education**: Educational level of parents
- **Social factors**: Extra-curricular activities, internet access, etc.
- **Behavioral factors**: Alcohol consumption, free time activities, health status

This project uses **Multiple Linear Regression** to model the relationship between these factors and final grades (G3), providing insights into which factors have the most significant impact on student success.

---

## Dataset

**Source**: Student Performance Dataset (UCI Machine Learning Repository)
- **Domain**: Education
- **Dataset**: Student Math Performance (student-mat.csv)
- **Samples**: ~395 students
- **Features**: 33 attributes including demographic, social, and academic factors

### Key Variables:
- **Target Variable**: `G3` (Final grade, range: 0-20)
- **Intermediate Grades**: `G1`, `G2` (First and second period grades)
- **Demographic**: age, sex, address, family size
- **Family Background**: Parental education (Medu, Fedu), parental jobs (Mjob, Fjob)
- **Academic**: study time, failures, school support, educational aspirations
- **Social**: extra activities, internet access, romantic relationships
- **Behavioral**: going out, alcohol consumption, health status, absences

---

## Project Structure

```
q4/
├── main.py                      # Main execution script
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── model/
│   └── linear_regression.py    # StudentPerformancePredictor class
├── utils/
│   ├── data_loader.py          # Data loading and preprocessing
│   └── evaluation.py           # Model evaluation and visualization
└── output/
    ├── predictions.csv          # Actual vs predicted grades
    ├── feature_coefficients.csv # Feature importance rankings
    ├── feature_group_analysis.csv # Group-wise analysis
    ├── evaluation_metrics.txt   # Performance metrics
    ├── model_summary.txt        # Comprehensive summary
    └── visualizations/          # All generated plots
        ├── actual_vs_predicted.png
        ├── residual_analysis.png
        ├── feature_importance.png
        ├── feature_group_importance.png
        ├── correlation_matrix.png
        └── grade_distribution.png
```

---

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup

1. **Navigate to project directory:**
   ```bash
   cd "C:\C programing\ADlab\day2\q4"
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install numpy pandas scikit-learn matplotlib seaborn
   ```

---

## Usage

### Run the complete analysis:
```bash
python main.py
```

### Output:
The script will:
1. Load and preprocess the student performance dataset
2. Train a Linear Regression model
3. Generate predictions and evaluate performance
4. Analyze feature importance and group contributions
5. Create 6 visualizations
6. Save all results to the `output/` directory

### Expected Runtime:
- **Dataset Loading**: ~5-10 seconds
- **Training**: ~1 second
- **Evaluation & Visualization**: ~10-15 seconds
- **Total**: ~20-30 seconds

---

## Methodology

### 1. Data Preprocessing
- **Encoding categorical variables**: Binary and label encoding for categorical features
- **Creating derived features**:
  - Study efficiency score
  - Average parental education
  - Grade improvement trend
- **Handling missing values**: Median imputation for numeric features
- **Feature normalization**: StandardScaler for consistent scaling

### 2. Feature Engineering
Features are grouped into five categories:
- **Demographic**: Age, sex, address, family size, parental status
- **Family Background**: Parental education, jobs, guardian
- **Academic**: Study time, failures, school support, aspirations
- **Social**: Family support, extra activities, internet, relationships
- **Behavioral**: Travel time, going out, alcohol consumption, absences

### 3. Model Training
- **Algorithm**: Linear Regression with feature standardization
- **Split Ratio**: 80% training, 20% testing
- **Random State**: 42 (for reproducibility)

### 4. Evaluation Metrics
- **R² Score**: Proportion of variance explained
- **MAE (Mean Absolute Error)**: Average prediction error in grade points
- **RMSE (Root Mean Squared Error)**: Standard deviation of residuals
- **MAPE (Mean Absolute Percentage Error)**: Percentage error
- **Accuracy Tolerance**: % of predictions within 1 and 2 grade points

### 5. Feature Importance Analysis
- **Individual Features**: Ranked by absolute coefficient values
- **Feature Groups**: Aggregated importance by category
- **Impact Direction**: Positive vs negative influence

---

## Key Features

### 1. Comprehensive Data Pipeline
- Automatic dataset loading from online sources
- Robust preprocessing with error handling
- Multiple encoding strategies for different variable types

### 2. Advanced Feature Engineering
- Derived features capturing student behavior patterns
- Group-based feature analysis
- Correlation analysis across all variables

### 3. Multiple Evaluation Metrics
- Statistical metrics (R², MAE, RMSE, MAPE)
- Practical accuracy measures (tolerance-based)
- Residual analysis for model diagnosis

### 4. Rich Visualizations
- Actual vs Predicted scatter plots
- Residual distribution analysis
- Feature importance bar charts
- Feature group comparison
- Correlation heatmaps
- Grade distribution comparisons

### 5. Detailed Reporting
- CSV files for all predictions and analyses
- Text summaries with key findings
- Comprehensive model documentation

---

## Results

### Expected Performance Metrics
- **R² Score**: 0.70 - 0.85 (explains 70-85% of variance)
- **Mean Absolute Error**: 1.0 - 2.0 grade points
- **Predictions within 1 point**: 50-65%
- **Predictions within 2 points**: 75-90%

### Top Influential Factors (Expected)
1. **Failures**: Number of past class failures (strong negative impact)
2. **Higher Education**: Desire for higher education (positive impact)
3. **Parental Education**: Mother's and father's education level (positive)
4. **Study Time**: Weekly study hours (positive)
5. **School Support**: Extra educational support (positive)
6. **Absences**: Number of school absences (negative)
7. **Going Out**: Frequency of going out with friends (negative)
8. **Alcohol Consumption**: Weekend/weekday alcohol use (negative)

### Feature Group Rankings (Expected)
1. **Academic Factors**: Highest impact on performance
2. **Family Background**: Strong influence through education and support
3. **Behavioral Factors**: Significant negative correlations
4. **Social Factors**: Moderate impact on outcomes
5. **Demographic Factors**: Lesser but notable influence

---

## Insights

### Key Findings

1. **Academic History is Most Predictive**
   - Past failures strongly predict future performance
   - Educational aspirations are critical motivators

2. **Parental Education Matters**
   - Higher parental education correlates with better student outcomes
   - Both mother's and father's education contribute significantly

3. **Study Habits Trump Raw Time**
   - Quality of study (study efficiency) is more important than just hours
   - Regular attendance outweighs occasional long study sessions

4. **Social Support Systems**
   - Family support and school support both enhance performance
   - Internet access enables better learning opportunities

5. **Behavioral Red Flags**
   - High absence rates are strong negative indicators
   - Excessive social activities (going out) can detract from studies
   - Alcohol consumption correlates with lower grades

6. **Socioeconomic Factors**
   - Family economic status influences resources and opportunities
   - Urban vs rural location shows measurable differences

### Practical Applications

**For Educators:**
- Identify at-risk students early based on key indicators
- Prioritize interventions for students with past failures
- Encourage parental involvement in education

**For Students:**
- Focus on consistent study habits over cramming
- Maintain regular attendance
- Balance social life with academic commitments

**For Policymakers:**
- Invest in support systems (tutoring, counseling)
- Address socioeconomic barriers to education
- Promote parental education programs

---

## Requirements

### Python Packages
```
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
```

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: ~100MB for dataset and outputs

---

## Future Enhancements

1. **Model Improvements**
   - Feature selection techniques (Lasso, Ridge regularization)
   - Polynomial features for non-linear relationships
   - Ensemble methods (Random Forest, Gradient Boosting)

2. **Advanced Analytics**
   - Student clustering based on performance patterns
   - Temporal analysis using G1, G2, G3 progression
   - Interaction effects between features

3. **Interactive Dashboards**
   - Web-based visualization interface
   - Real-time prediction tool for new students
   - What-if scenario analysis

4. **Cross-Dataset Validation**
   - Test on Portuguese language performance dataset
   - Compare across different schools and regions
   - Validate findings on international datasets

---

## References

1. P. Cortez and A. Silva. Using Data Mining to Predict Secondary School Student Performance. In A. Brito and J. Teixeira Eds., Proceedings of 5th FUture BUsiness TEChnology Conference (FUBUTEC 2008) pp. 5-12, Porto, Portugal, April, 2008, EUROSIS, ISBN 978-9077381-39-7.

2. UCI Machine Learning Repository: Student Performance Data Set
   https://archive.ics.uci.edu/ml/datasets/Student+Performance

---

## License
This project is for educational purposes as part of Advanced Data Analytics Lab coursework.

---

## Contact
For questions or suggestions regarding this analysis, please contact through the course repository.

---

**Last Updated**: December 2025
