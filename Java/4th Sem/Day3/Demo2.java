import java.util.Scanner;

class Rectangle {
    double length;
    double breadth;

    public void perimeter() {
        double perimeter = 2 * (length + breadth);
        System.out.println("The perimeter of the rectangle is: " + perimeter);
    }

    public void area() {
        double area = length * breadth;
        System.out.println("The area of the rectangle is: " + area);
    }
}

public class Demo2 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in); 
        Rectangle rectangle = new Rectangle();

        System.out.print("Enter the length of the rectangle: ");
        rectangle.length = scanner.nextDouble();

        System.out.print("Enter the breadth of the rectangle: ");
        rectangle.breadth = scanner.nextDouble();

        rectangle.perimeter();
        rectangle.area();

        scanner.close();
    }
}
