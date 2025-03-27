package Marketing;
import General.Employee;

public class Sales extends Employee {
    public Sales(int empId, String eName) {
        super(empId, eName);
    }
    
    public double tAllowance(double earnings) {
        return 0.05 * earnings;
    }
}
