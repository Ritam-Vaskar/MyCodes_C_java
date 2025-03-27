package General;

public class Employee {
    protected int empId;
    private String eName;
    
    public Employee(int empId, String eName) {
        this.empId = empId;
        this.eName = eName;
    }
    
    public double earnings(double basic) {
        return basic + (0.8 * basic) + (0.15 * basic);
    }
}