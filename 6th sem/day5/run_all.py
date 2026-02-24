"""
Run All Day 5 Implementations
Executes both Q1 and Q2 with proper separation
"""

import subprocess
import sys
import os


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*80)
    print(text.center(80))
    print("="*80 + "\n")


def run_script(script_name, question_num):
    """Run a Python script and capture output"""
    print_header(f"RUNNING {question_num}")
    
    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True,
            check=True
        )
        
        print_header(f"{question_num} COMPLETED SUCCESSFULLY")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running {script_name}")
        print(f"Error: {e}")
        return False
    except FileNotFoundError:
        print(f"\n❌ File not found: {script_name}")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print_header("CHECKING DEPENDENCIES")
    
    required_packages = ['matplotlib', 'networkx', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠ Missing packages: {', '.join(missing_packages)}")
        print("\nTo install missing packages, run:")
        print("  pip install -r requirements.txt")
        print("\nOr install individually:")
        for pkg in missing_packages:
            print(f"  pip install {pkg}")
        return False
    
    print("\n✓ All dependencies are installed!")
    return True


def main():
    """Main function to run all implementations"""
    print_header("DAY 5 - GRAPH SEARCH ALGORITHMS")
    print("This script will run both Q1 and Q2 implementations")
    print("\nQ1: City Map Shortest Path - Bi-directional BFS")
    print("Q2: Treasure Hunt - Best-First Search")
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot proceed without required dependencies.")
        return
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # Run Q1
    q1_success = run_script(
        "q1_city_map_shortest_path.py",
        "Q1: City Map Shortest Path"
    )
    
    # Run Q2
    q2_success = run_script(
        "q2_treasure_hunt_best_first_search.py",
        "Q2: Treasure Hunt"
    )
    
    # Summary
    print_header("EXECUTION SUMMARY")
    
    if q1_success and q2_success:
        print("✓ All implementations executed successfully!")
        print("\nGenerated files:")
        print("\nQ1 Output Files:")
        print("  - city_map_test_case_1.png")
        print("  - city_map_test_case_2.png")
        print("  - city_map_test_case_3.png")
        print("  - algorithm_comparison.png")
        print("\nQ2 Output Files:")
        print("  - scenario1_heuristic.png")
        print("  - scenario1_result.png")
        print("  - scenario2_heuristic.png")
        print("  - scenario2_result.png")
        print("  - scenario3_heuristic.png")
        print("  - scenario3_result.png")
        print("\nCheck the generated PNG files for visualizations!")
    else:
        print("❌ Some implementations failed to execute.")
        if not q1_success:
            print("  - Q1 failed")
        if not q2_success:
            print("  - Q2 failed")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
