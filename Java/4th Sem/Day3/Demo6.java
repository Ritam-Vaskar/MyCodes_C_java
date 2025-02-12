import java.util.Scanner;


class Rectangle {
   
    private double length;
    private double breadth;


    public Rectangle() {
        this.length = 0;
        this.breadth = 0;
    }

 
    public Rectangle(double length, double breadth) {
        this.length = length;
        this.breadth = breadth;
    }

    
    public double calculateArea() {
        return length * breadth;
    }

    
    public void displayDetails() {
        System.out.println("Length: " + length + ", Breadth: " + breadth);
        System.out.println("Area of the rectangle: " + calculateArea());
    }
}


public class Demo6
{
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        
        Rectangle defaultRectangle = new Rectangle();
        System.out.println("Default rectangle:");
        defaultRectangle.displayDetails();

        
        System.out.print("\nEnter the length of the rectangle: ");
        double length = scanner.nextDouble();
        System.out.print("Enter the breadth of the rectangle: ");
        double breadth = scanner.nextDouble();

        Rectangle userRectangle = new Rectangle(length, breadth);
        System.out.println("\nUser-defined rectangle:");
        userRectangle.displayDetails();

        scanner.close();
    }
}