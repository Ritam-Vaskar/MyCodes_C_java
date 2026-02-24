"""
AD Lab Day 7: Run All Questions
Executes all questions sequentially and provides a comprehensive summary
"""

import subprocess
import time
import os
import sys

# Create main output directory
os.makedirs("output", exist_ok=True)

print("=" * 80)
print(" " * 20 + "AD LAB DAY 7: NEURAL NETWORKS AND PSO")
print("=" * 80)
print()

# Define all questions
questions = [
    {
        'id': 'q1',
        'name': 'Basic MNIST Data Handling and Model Construction',
        'file': 'q1.py',
        'description': 'Load MNIST, normalize, build and train basic neural network'
    },
    {
        'id': 'q2',
        'name': 'PSO for Weight Optimization',
        'file': 'q2.py',
        'description': 'Use PSO to optimize neural network weights instead of backprop'
    },
    {
        'id': 'q3',
        'name': 'Performance Analysis and Model Improvements',
        'file': 'q3.py',
        'description': 'Training plots, dropout, architecture changes, confusion matrix'
    },
    {
        'id': 'q4',
        'name': 'PSO for Hyperparameter Optimization',
        'file': 'q4.py',
        'description': 'Optimize neurons, learning rate, batch size, dropout using PSO'
    },
    {
        'id': 'q5',
        'name': 'PSO-based Neural Architecture Search',
        'file': 'q5.py',
        'description': 'Automated architecture search: layers, neurons, activation'
    }
]

results = []
total_start_time = time.time()

# Run each question
for i, q in enumerate(questions, 1):
    print(f"\n{'=' * 80}")
    print(f"RUNNING QUESTION {i}/{len(questions)}: {q['name']}")
    print(f"Description: {q['description']}")
    print(f"{'=' * 80}\n")
    
    start_time = time.time()
    
    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, q['file']],
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            status = "[SUCCESS]"
            print(f"\n{status} - Completed in {elapsed_time:.1f}s ({elapsed_time/60:.1f} min)")
        else:
            status = "[FAILED]"
            print(f"\n{status} - Error occurred")
            print(f"Error output:\n{result.stderr}")
        
        results.append({
            'question': q['name'],
            'id': q['id'],
            'status': status,
            'time': elapsed_time,
            'success': result.returncode == 0
        })
        
    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        status = "[TIMEOUT]"
        print(f"\n{status} - Exceeded 1 hour limit")
        results.append({
            'question': q['name'],
            'id': q['id'],
            'status': status,
            'time': elapsed_time,
            'success': False
        })
    
    except Exception as e:
        elapsed_time = time.time() - start_time
        status = "[ERROR]"
        print(f"\n{status} - Exception: {str(e)}")
        results.append({
            'question': q['name'],
            'id': q['id'],
            'status': status,
            'time': elapsed_time,
            'success': False
        })

total_time = time.time() - total_start_time

# Print summary
print("\n" + "=" * 80)
print(" " * 30 + "EXECUTION SUMMARY")
print("=" * 80)
print()

print(f"{'Question':<50} {'Status':<15} {'Time':<15}")
print("-" * 80)

for r in results:
    time_str = f"{r['time']:.1f}s ({r['time']/60:.1f}m)"
    print(f"{r['question']:<50} {r['status']:<15} {time_str:<15}")

print("-" * 80)
print(f"{'TOTAL':<50} {'':<15} {total_time:.1f}s ({total_time/60:.1f}m)")
print()

# Success rate
successful = sum(1 for r in results if r['success'])
total = len(results)
success_rate = (successful / total) * 100

print(f"Success Rate: {successful}/{total} ({success_rate:.0f}%)")
print()

# Output locations
print("Output Locations:")
for q in questions:
    output_path = f"output/{q['id']}/"
    if os.path.exists(output_path):
        files = os.listdir(output_path)
        print(f"  {q['id']}: {len(files)} files in {output_path}")

print()
print("=" * 80)

# Save summary to file
with open("output/execution_summary.txt", 'w', encoding='utf-8') as f:
    f.write("AD Lab Day 7 - Execution Summary\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Total Execution Time: {total_time:.1f}s ({total_time/60:.1f} minutes)\n")
    f.write(f"Success Rate: {successful}/{total} ({success_rate:.0f}%)\n\n")
    f.write(f"{'Question':<50} {'Status':<15} {'Time':<15}\n")
    f.write("-" * 80 + "\n")
    for r in results:
        time_str = f"{r['time']:.1f}s"
        f.write(f"{r['question']:<50} {r['status']:<15} {time_str:<15}\n")

print("Summary saved to: output/execution_summary.txt")
print("=" * 80)

if successful == total:
    print("\n[SUCCESS] All questions completed successfully!")
else:
    print(f"\n[WARNING] {total - successful} question(s) failed. Check output above for details.")
