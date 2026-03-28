"""
Day 8: CNN with CIFAR-10 - Run All Questions
Executes all 10 questions sequentially
"""

import subprocess
import sys
import time
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def run_question(q_num, description):
    """Run a single question"""
    print_header(f"Q{q_num}: {description}")
    
    q_dir = Path(f"q{q_num}")
    main_file = q_dir / "main.py"
    
    if not main_file.exists():
        print(f"❌ {main_file} not found. Skipping...")
        return False
    
    start_time = time.time()
    
    try:
        # Run the question
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=str(q_dir),
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout per question
        )
        
        elapsed_time = time.time() - start_time
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            print(f"\n✅ Q{q_num} completed successfully in {elapsed_time:.1f}s")
            return True
        else:
            print(f"\n❌ Q{q_num} failed with error code {result.returncode}")
            if result.stderr:
                print("Error output:")
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        print(f"\n⏱️ Q{q_num} timed out after {elapsed_time:.1f}s")
        return False
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"\n❌ Q{q_num} failed with exception: {e}")
        return False

def main():
    print_header("DAY 8: CNN WITH CIFAR-10 - ALL QUESTIONS")
    
    start_time = time.time()
    
    questions = [
        (1, "Data Loading, Visualization, and Normalization"),
        (2, "One-Hot Encoding vs Sparse Categorical"),
        (3, "Build Simple CNN Model"),
        (4, "Modified CNN with Second Conv2D Layer"),
        (5, "Train CNN with Validation Split"),
        (6, "Add Dropout Regularization"),
        (7, "Add Batch Normalization"),
        (8, "Increase Filter Sizes (32→64→128)"),
        (9, "Use Early Stopping"),
        (10, "Confusion Matrix & Misclassified Images")
    ]
    
    results = []
    
    for q_num, description in questions:
        success = run_question(q_num, description)
        results.append((q_num, description, success))
        
        if not success:
            print(f"\n⚠️ Warning: Q{q_num} failed. Continuing to next question...")
            time.sleep(1)
    
    # Print summary
    total_time = time.time() - start_time
    
    print_header("EXECUTION SUMMARY")
    
    successful = sum(1 for _, _, success in results if success)
    failed = len(results) - successful
    
    print(f"Total Questions: {len(results)}")
    print(f"Successful: {successful} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Total Time: {total_time:.1f}s ({total_time/60:.1f} minutes)\n")
    
    print("Detailed Results:")
    for q_num, description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  Q{q_num:2d}: {status} - {description}")
    
    print("\n" + "=" * 70)
    
    if failed == 0:
        print("🎉 All questions completed successfully!")
    else:
        print(f"⚠️ {failed} question(s) failed. Check the output above for details.")
    
    print("=" * 70 + "\n")
    
    # Save execution summary
    with open("output/execution_summary.txt", "w", encoding="utf-8") as f:
        f.write("Day 8 Execution Summary\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total Questions: {len(results)}\n")
        f.write(f"Successful: {successful}\n")
        f.write(f"Failed: {failed}\n")
        f.write(f"Total Time: {total_time:.1f}s\n\n")
        f.write("Results:\n")
        for q_num, description, success in results:
            status = "PASS" if success else "FAIL"
            f.write(f"  Q{q_num:2d}: {status} - {description}\n")
    
    print("📄 Execution summary saved to output/execution_summary.txt")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    try:
        import os
        os.makedirs("output", exist_ok=True)
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Execution interrupted by user.")
        sys.exit(1)
