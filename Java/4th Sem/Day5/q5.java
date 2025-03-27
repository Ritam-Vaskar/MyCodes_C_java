import General.Employee;
import Marketing.Sales;
import java.util.Scanner;

public class q5 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Enter the employee id and employee name:");
        int empId = scanner.nextInt();
        String eName = scanner.next();
        
        System.out.println("Enter the basic salary:");
        double basicSalary = scanner.nextDouble();
        
        Sales salesPerson = new Sales(empId, eName);
        double totalEarnings = salesPerson.earnings(basicSalary);
        double travelAllowance = salesPerson.tAllowance(totalEarnings);
        
        System.out.println("The emp id of the employee is " + empId);
        System.out.println("The total earning is " + (totalEarnings + travelAllowance));
    }
}
