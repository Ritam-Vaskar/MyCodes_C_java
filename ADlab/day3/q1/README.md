# Q1: Spam Email Classification using Logistic Regression

## Overview
Binary classification of emails as spam or non-spam using Logistic Regression with TF-IDF features.

## Problem Statement
Build a logistic regression model to classify emails, assess performance using:
- **Accuracy**: Percentage of correctly classified emails
- **Confusion Matrix**: True/False positives and negatives
- **Classification Report**: Precision, Recall, F1-score for both classes

## Dataset
- **Source**: SMS Spam Collection Dataset (UCI Machine Learning Repository)
- **URL**: https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv
- **Total Messages**: 5,572 SMS messages
- **Distribution**: 
  - Spam: 747 (13.41%)
  - Non-spam (Ham): 4,825 (86.59%)
- **Features**: TF-IDF vectorization (1000 features max)
- **Note**: Automatically downloads from GitHub on first run

## Model
- **Algorithm**: Logistic Regression
- **Feature Extraction**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Train-Test Split**: 80-20 with stratification

## Project Structure
```
q1/
├── main.py                          # Main execution script
├── model/
│   └── logistic_regression_model.py # Spam classifier class
├── utils/
│   └── data_loader.py              # Data generation
├── output/                          # Results and visualizations
├── README.md                        # This file
└── requirements.txt                 # Dependencies
```

## Installation

```bash
cd "C:\C programing\ADlab\day3\q1"
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Output

### 1. Console Output
- Dataset statistics
- Training progress
- **Accuracy score**
- **Confusion matrix**
- **Classification report** (Precision, Recall, F1-score)

### 2. Files Generated
- `output/predictions.csv` - Predictions for each test email
- `output/metrics.txt` - Detailed performance metrics
- `output/spam_classification_results.png` - 4-panel visualization

### 3. Visualizations
1. **Confusion Matrix Heatmap**
2. **Class Distribution** (Actual vs Predicted)
3. **Top 10 Spam Indicators** (words strongly predicting spam)
4. **Top 10 Non-Spam Indicators** (words strongly predicting non-spam)

## Key Metrics

| Metric | Description |
|--------|-------------|
| **Accuracy** | Overall correct classifications |
| **Precision** | Of predicted spam, how many are actually spam |
| **Recall** | Of actual spam, how many were caught |
| **F1-Score** | Harmonic mean of precision and recall |

## Algorithm

### 1. Data Preprocessing
```
1. Generate synthetic emails with spam/ham keywords
2. Split into train (80%) and test (20%)
3. Convert text to TF-IDF features
```

### 2. Model Training
```
1. Initialize TfidfVectorizer (max_features=500)
2. Fit vectorizer on training emails
3. Train LogisticRegression on TF-IDF features
```

### 3. Evaluation
```
1. Transform test emails to TF-IDF
2. Predict labels
3. Calculate metrics:
   - Accuracy = (TP + TN) / Total
   - Precision = TP / (TP + FP)
   - Recall = TP / (TP + FN)
   - F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

## Expected Results

**Performance on Real SMS Spam Dataset:**
- **Accuracy: ~97.40%**
- **Precision (Spam): ~1.00** (perfect - no false positives)
- **Recall (Spam): ~0.81** (catches 81% of spam)
- **F1-Score (Spam): ~0.89**

**Note**: Imbalanced dataset (13% spam) makes recall more important than precision for spam detection.

## Features

### Spam Indicators (High Positive Coefficients)
- free, win, cash, prize, click, buy, urgent, discount

### Non-Spam Indicators (High Negative Coefficients)
- meeting, schedule, report, project, team, attached, regarding

## Requirements
```
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
```

---

**Date:** December 16, 2025  
**Status:** Complete ✓
