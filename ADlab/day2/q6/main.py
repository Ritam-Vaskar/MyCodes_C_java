"""Q6 - Triple Analysis Combined Runner"""
import os, sys

def run_analysis(folder, name):
    print("\n" + "#"*80)
    print(f" {name} ".center(80, "#"))
    print("#"*80 + "\n")
    
    os.chdir(folder)
    sys.path.insert(0, os.getcwd())
    
    try:
        import main as analysis_main
        analysis_main.main()
    finally:
        os.chdir("..")
        sys.path.pop(0)

def main():
    print("\n" + "="*80)
    print(" Q6: TRIPLE LINEAR REGRESSION ANALYSIS ".center(80))
    print("="*80)
    print("\n1. Medical Cost Personal Dataset")
    print("2. Loan Default Rates Analysis")
    print("3. Unemployment Rates Analysis")
    print("="*80 + "\n")
    
    analyses = [
        ("medical_cost", "MEDICAL COST PERSONAL ANALYSIS"),
        ("loan_default", "LOAN DEFAULT RATES ANALYSIS"),
        ("unemployment", "UNEMPLOYMENT RATES ANALYSIS")
    ]
    
    for folder, name in analyses:
        input(f"Press Enter to run {name}...")
        try:
            run_analysis(folder, name)
        except Exception as e:
            print(f"\n[!] Error in {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print(" ALL THREE ANALYSES COMPLETE ".center(80))
    print("="*80)
    print("\nResults:")
    print("  - Medical Cost: medical_cost/output/")
    print("  - Loan Default: loan_default/output/")
    print("  - Unemployment: unemployment/output/")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
