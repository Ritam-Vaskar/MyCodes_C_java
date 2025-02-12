// // package Java.4th Sem.Day5;
// Define an interface Emploee with a method getDetails() to get emplyee
// details as Empid and Ename. Also define a derived interface Manager with a method
// getDeptDetails() to get department details such as Deptid and Deptname.Then define a class Head
// which implements Manager interface and also prints all details of the employee. Write the complete
// program to display all details of one head of the department.
// Input - Enter employee id - 123
// Enter employee name - Sidharth Ambani
// Enter department id - 06
// Enter department name -Marketing
// Output - Employee id - 123
// Employee name - Sidharth Ambani
// Department id - 06
// Department name -Marketing

interface Employee{
    void getDetails();
}
interface Manager extends Employee{
    void getDeptDetails();
}
class Head implements Manager{
    public void getDetails(){
        System.out.println("Employee id - 123");
        System.out.println("Employee name - Sidharth Ambani");
    }
    public void getDeptDetails(){
        System.out.println("Department id - 06");
        System.out.println("Department name -Marketing");
    }
}


public class q4 {
    public static void main(String[] args) {
        Head h = new Head();
        h.getDetails();
        h.getDeptDetails();
    }
}
