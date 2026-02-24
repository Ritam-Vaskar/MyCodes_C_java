"""
Setup script for AD Lab Day 7
Installs all required dependencies
"""

import subprocess
import sys
import os

print("=" * 80)
print(" " * 25 + "AD LAB DAY 7 - SETUP")
print("=" * 80)
print()

# Check Python version
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print()

# List of required packages
packages = [
    'tensorflow>=2.13.0',
    'numpy>=1.24.3',
    'matplotlib>=3.7.1',
    'scikit-learn>=1.3.0',
    'seaborn>=0.12.2',
    'pandas>=2.0.3'
]

print("Installing required packages...")
print("-" * 80)

failed_packages = []

for i, package in enumerate(packages, 1):
    package_name = package.split('>=')[0]
    print(f"\n[{i}/{len(packages)}] Installing {package}...")
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print(f"    SUCCESS: {package_name} installed")
        else:
            print(f"    FAILED: {package_name}")
            print(f"    Error: {result.stderr[:200]}")
            failed_packages.append(package_name)
    
    except subprocess.TimeoutExpired:
        print(f"    TIMEOUT: {package_name} installation took too long")
        failed_packages.append(package_name)
    
    except Exception as e:
        print(f"    ERROR: {package_name} - {str(e)}")
        failed_packages.append(package_name)

print()
print("=" * 80)
print(" " * 30 + "SETUP SUMMARY")
print("=" * 80)

if not failed_packages:
    print()
    print("SUCCESS: All packages installed successfully!")
    print()
    print("Next steps:")
    print("  1. Run all questions: python run_all.py")
    print("  2. Or run individual questions: python q1.py, python q2.py, etc.")
    print()
else:
    print()
    print(f"WARNING: {len(failed_packages)} package(s) failed to install:")
    for pkg in failed_packages:
        print(f"  - {pkg}")
    print()
    print("Please try installing them manually:")
    for pkg in failed_packages:
        print(f"  python -m pip install {pkg}")
    print()

print("=" * 80)

# Test imports
print()
print("Testing imports...")
print("-" * 80)

test_imports = [
    ('tensorflow', 'TensorFlow'),
    ('numpy', 'NumPy'),
    ('matplotlib', 'Matplotlib'),
    ('sklearn', 'scikit-learn'),
    ('seaborn', 'Seaborn'),
    ('pandas', 'Pandas')
]

all_imports_ok = True

for module_name, display_name in test_imports:
    try:
        __import__(module_name)
        print(f"OK: {display_name}")
    except ImportError:
        print(f"FAILED: {display_name} - not installed or not importable")
        all_imports_ok = False

print()
if all_imports_ok:
    print("SUCCESS: All packages are importable!")
    print()
    print("You're ready to run the lab!")
    print("Run: python run_all.py")
else:
    print("WARNING: Some packages failed to import")
    print("Please check the errors above and reinstall failed packages")

print("=" * 80)
