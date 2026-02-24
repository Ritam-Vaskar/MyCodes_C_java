# Quick Start Instructions

## Step 1: Install Dependencies

Run ONE of these commands in PowerShell:

```powershell
# Option 1: Using the setup script (recommended)
python setup.py

# Option 2: Direct installation
python -m pip install tensorflow numpy matplotlib scikit-learn seaborn pandas

# Option 3: From requirements file
python -m pip install -r requirements.txt
```

**Note:** If you see "pip is not recognized", always use `python -m pip` instead of just `pip`.

## Step 2: Run the Lab

```powershell
# Run all questions (takes 45-75 minutes)
python run_all.py

# Or run individual questions
python q1.py   # ~2 minutes
python q2.py   # ~10 minutes
python q3.py   # ~15 minutes
python q4.py   # ~20 minutes
python q5.py   # ~20 minutes
```

## Troubleshooting

### "No module named 'tensorflow'"
- You need to install the dependencies first (see Step 1)
- Make sure installation completed without errors

### "pip is not recognized"
- Use `python -m pip` instead of `pip`
- Example: `python -m pip install tensorflow`

### Installation takes too long
- Normal! TensorFlow is a large package
- Can take 5-10 minutes depending on internet speed
- Be patient and let it finish

### Out of memory errors
- Close other applications
- Reduce dataset size in the code if needed

## What to Expect

After successful installation:
- Q1 trains a basic neural network (~97% accuracy)
- Q2 compares PSO vs Adam optimizer
- Q3 analyzes model performance improvements
- Q4 optimizes hyperparameters using PSO
- Q5 searches for best architecture using PSO

Total runtime: 45-75 minutes for all questions.

All outputs saved to: `output/q1/`, `output/q2/`, etc.
