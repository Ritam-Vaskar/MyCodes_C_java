"""
Q5 - Combined Analysis Script
Runs both Car Mileage and Health Insurance analyses
"""

import os
import sys

def run_car_mileage_analysis():
    """Run Car Mileage Prediction Analysis"""
    print("\n" + "#"*80)
    print(" PART 1: CAR MILEAGE PREDICTION ANALYSIS ".center(80, "#"))
    print("#"*80 + "\n")
    
    os.chdir("car_mileage")
    sys.path.insert(0, os.getcwd())
    
    try:
        from car_mileage.main import main as car_main
        car_main()
    except ImportError:
        import main as car_main_module
        car_main_module.main()
    finally:
        os.chdir("..")
        sys.path.pop(0)

def run_insurance_analysis():
    """Run Health Insurance Charges Analysis"""
    print("\n" + "#"*80)
    print(" PART 2: HEALTH INSURANCE CHARGES ANALYSIS ".center(80, "#"))
    print("#"*80 + "\n")
    
    os.chdir("insurance_charges")
    sys.path.insert(0, os.getcwd())
    
    try:
        from insurance_charges.main import main as insurance_main
        insurance_main()
    except ImportError:
        import main as insurance_main_module
        insurance_main_module.main()
    finally:
        os.chdir("..")
        sys.path.pop(0)

def main():
    """Run both analyses"""
    print("\n" + "="*80)
    print(" Q5: DUAL LINEAR REGRESSION ANALYSIS ".center(80))
    print("="*80)
    print("\nThis script will run two separate analyses:")
    print("1. Car Mileage Prediction (Auto MPG Dataset)")
    print("2. Health Insurance Charges Prediction")
    print("="*80 + "\n")
    
    input("Press Enter to start Car Mileage Analysis...")
    
    try:
        run_car_mileage_analysis()
    except Exception as e:
        print(f"\n[!] Error in Car Mileage Analysis: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n")
    input("Press Enter to start Insurance Analysis...")
    
    try:
        run_insurance_analysis()
    except Exception as e:
        print(f"\n[!] Error in Insurance Analysis: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print(" BOTH ANALYSES COMPLETE ".center(80))
    print("="*80)
    print("\nResults:")
    print("  - Car Mileage: car_mileage/output/")
    print("  - Insurance: insurance_charges/output/")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
