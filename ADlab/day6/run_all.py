"""
Run all PCA projects in sequence
This script executes all 10 questions one by one and provides a summary.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def run_question(question_num):
    """Run a specific question's main.py"""
    question_dir = Path(f"q{question_num}")
    main_file = question_dir / "main.py"
    
    if not main_file.exists():
        print(f"❌ Question {question_num}: main.py not found")
        return False
    
    print(f"\n{'='*70}")
    print(f"RUNNING QUESTION {question_num}")
    print(f"{'='*70}\n")
    
    start_time = time.time()
    
    try:
        # Change to question directory and run
        os.chdir(question_dir)
        result = subprocess.run([sys.executable, "main.py"], 
                              capture_output=False, 
                              text=True,
                              check=True)
        os.chdir("..")
        
        elapsed = time.time() - start_time
        print(f"\n✅ Question {question_num} completed in {elapsed:.2f} seconds")
        return True
        
    except subprocess.CalledProcessError as e:
        os.chdir("..")
        elapsed = time.time() - start_time
        print(f"\n❌ Question {question_num} failed after {elapsed:.2f} seconds")
        print(f"Error: {e}")
        return False
    except Exception as e:
        os.chdir("..")
        elapsed = time.time() - start_time
        print(f"\n❌ Question {question_num} encountered an error after {elapsed:.2f} seconds")
        print(f"Error: {e}")
        return False

def main():
    """Run all questions"""
    print("="*70)
    print("PCA ANALYSIS - RUNNING ALL QUESTIONS")
    print("="*70)
    print("\nThis will run all 10 PCA analysis questions sequentially.")
    print("Each question will generate outputs in its respective output/ directory.")
    print("\nPress Ctrl+C to cancel...\n")
    
    time.sleep(2)
    
    start_time = time.time()
    results = {}
    
    questions = [
        "Q1: Wine Dataset PCA Visualization",
        "Q2: Breast Cancer SVM with PCA",
        "Q3: Fraud Detection with Imbalanced Data",
        "Q4: Intrusion Detection Timing Analysis",
        "Q5: Digit Recognition Optimal Components",
        "Q6: Noisy Clinical Features Robustness",
        "Q7: Spam Detection with TF-IDF",
        "Q8: Plant Disease Classification",
        "Q9: Eye State Detection - SVM vs KNN",
        "Q10: Land Cover Remote Sensing"
    ]
    
    for i in range(1, 11):
        results[i] = run_question(i)
        
        # Small pause between questions
        if i < 10:
            time.sleep(1)
    
    # Summary
    total_time = time.time() - start_time
    
    print("\n" + "="*70)
    print("EXECUTION SUMMARY")
    print("="*70)
    
    successful = sum(1 for v in results.values() if v)
    failed = len(results) - successful
    
    print(f"\nTotal questions: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total execution time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    
    print("\nDetailed Results:")
    for i, (question_num, success) in enumerate(results.items(), 1):
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {status} - {questions[i-1]}")
    
    if failed == 0:
        print("\n🎉 All questions completed successfully!")
        print("Check each question's output/ directory for results.")
    else:
        print(f"\n⚠️  {failed} question(s) failed. Please check the error messages above.")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execution cancelled by user.")
        sys.exit(1)
