import java.util.Scanner;

class Account {
    protected int acc_no;
    protected double balance;

    
    public void input(Scanner scanner) {
        System.out.print("Enter account number: ");
        acc_no = scanner.nextInt();
        System.out.print("Enter account balance: ");
        balance = scanner.nextDouble();
    }

   
    public void disp() {
        System.out.println("Account Number: " + acc_no);
        System.out.println("Balance: " + balance);
    }
}


class Person extends Account {
    private String name;
    private String aadhar_no;

    
    @Override
    public void input(Scanner scanner) {
        super.input(scanner); 
        scanner.nextLine(); 
        System.out.print("Enter name: ");
        name = scanner.nextLine();
        System.out.print("Enter Aadhar number: ");
        aadhar_no = scanner.nextLine();
    }

    
    @Override
    public void disp() {
        System.out.println("Name: " + name);
        System.out.println("Aadhar Number: " + aadhar_no);
        super.disp(); 
    }
}


public class q4 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Person[] persons = new Person[3]; 

      
        for (int i = 0; i < persons.length; i++) {
            System.out.println("Enter details of person " + (i + 1) + ":");
            persons[i] = new Person(); 
            persons[i].input(scanner);
            System.out.println();
        }

        System.out.println("Details of persons:");
        for (int i = 0; i < persons.length; i++) {
            System.out.println("Person " + (i + 1) + ":");
            persons[i].disp();
            System.out.println();
        }

        scanner.close();
    }
}
