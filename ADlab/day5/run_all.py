"""
Run all clustering analysis scripts
"""

import os
import sys
import time
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

scripts = [
    ('q1.py', 'K-Means on Mall Customers'),
    ('q2.py', 'DBSCAN on Iris'),
    ('q3.py', 'K-Means vs Hierarchical on Wholesale'),
    ('q4.py', 'GMM vs K-Means on Iris'),
    ('q5.py', 'K-Means on Digits'),
    ('q6.py', 'Spectral Clustering on Iris'),
    ('q7.py', 'DBSCAN on Two Moons'),
    ('q8.py', 'Clustering Stability'),
    ('q9.py', 'PSO-Optimized K-Means'),
    ('q10.py', 'Fuzzy C-Means on Iris')
]

print("="*70)
print("RUNNING ALL CLUSTERING ANALYSES")
print("="*70)

total_start = time.time()
results = []

for script, description in scripts:
    print(f"\n{'='*70}")
    print(f"Running: {description} ({script})")
    print('='*70)
    
    start_time = time.time()
    
    try:
        exit_code = os.system(f'python {script}')
        elapsed = time.time() - start_time
        
        if exit_code == 0:
            status = "✓ SUCCESS"
            results.append((script, description, elapsed, "Success"))
        else:
            status = "✗ FAILED"
            results.append((script, description, elapsed, "Failed"))
        
        print(f"\n{status} - Completed in {elapsed:.2f} seconds")
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n✗ ERROR: {str(e)}")
        results.append((script, description, elapsed, f"Error: {str(e)}"))

total_elapsed = time.time() - total_start

print("\n" + "="*70)
print("EXECUTION SUMMARY")
print("="*70)

for script, description, elapsed, status in results:
    print(f"{script:12} - {description:35} - {elapsed:6.2f}s - {status}")

print(f"\nTotal execution time: {total_elapsed:.2f} seconds")
print(f"Successful: {sum(1 for r in results if 'Success' in r[3])}/{len(results)}")

# Save summary
with open('output/execution_summary.txt', 'w') as f:
    f.write("CLUSTERING ANALYSIS EXECUTION SUMMARY\n")
    f.write("="*70 + "\n\n")
    for script, description, elapsed, status in results:
        f.write(f"{script}: {description}\n")
        f.write(f"  Time: {elapsed:.2f}s\n")
        f.write(f"  Status: {status}\n\n")
    f.write(f"Total time: {total_elapsed:.2f} seconds\n")

print("\n✓ All analyses complete! Check individual output folders for results.")
