import java.util.Scanner;
class Student {
   int roll;
   String name;
   double cgpa;
    public Student(int roll, String name, double cgpa) {
        this.roll = roll;
        this.name = name;
        this.cgpa = cgpa;
    }

    public int getRoll() {
        return roll;
    }

    public String getName() {
        return name;
    }

    public double getCgpa() {
        return cgpa;
    }
    public void displayDetails() {
        System.out.println("Roll No: " + roll + ", Name: " + name + ", CGPA: " + cgpa);
    }
}
public class Demo3 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

       
        System.out.print("Enter the number of students: ");
        int n = scanner.nextInt();
        scanner.nextLine(); 
        Student[] students = new Student[n];
        for (int i = 0; i < n; i++) {
            System.out.println("Enter details for student " + (i + 1) + ":");
            System.out.print("Enter Roll No: ");
            int roll = scanner.nextInt();
            scanner.nextLine();

            System.out.print("Enter Name: ");
            String name = scanner.nextLine();

            System.out.print("Enter CGPA: ");
            double cgpa = scanner.nextDouble();

            students[i] = new Student(roll, name, cgpa);
        }
        System.out.println("\nDetails of all students:");
        for (Student student : students) {
            student.displayDetails();
        }
        Student lowestCgpaStudent = students[0];
        for (Student student : students) {
            if (student.getCgpa() < lowestCgpaStudent.getCgpa()) {
                lowestCgpaStudent = student;
            }
        }

        System.out.println("\nStudent with the lowest CGPA:");
        System.out.println("Name: " + lowestCgpaStudent.getName());
        scanner.close();
    }
}