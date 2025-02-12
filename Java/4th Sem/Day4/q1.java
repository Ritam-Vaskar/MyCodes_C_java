// A Plastic manufacturer sells plastic in different shapes like 2D sheet and 3D
// box. The cost of sheet is Rs 40/ per square ft. and the cost of box is Rs 60/ per cubic ft. Implement
// it in Java to calculate the cost of plastic as per the dimensions given by the user where 3D inherits
// from 2D.
// Input: Enter dimensions
// Output: Display the cost of plastic

import java.util.Scanner;


class Sheet {
    private double length;
    private double width;
    private final double costSqr = 40;

    public Sheet(double length, double width) {
        this.length = length;
        this.width = width;
    }

   
    public double calculateArea() {
        return length * width;
    }

    
    public double calCost() {
        return calculateArea() * costSqr;
    }
}


class Box extends Sheet {
    private double height;
    private final double costCubic = 60;

    public Box(double length, double width, double height) {
        super(length, width); 
        this.height = height;
    }

    
    public double calVol() {
        return calculateArea() * height; 
    }

    
    public double calCost() {
        return calVol() * costCubic;
    }
}

public class q1 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter the dimensions for the 2D sheet (length and width in feet):");
        double length = scanner.nextDouble();
        double width = scanner.nextDouble();
        Sheet sheet = new Sheet(length, width);
        System.out.printf("The cost of the 2D sheet is: Rs %.2f%n", sheet.calCost());

        System.out.println("Enter the dimensions for the 3D box (length, width, and height in feet):");
        double boxLength = scanner.nextDouble();
        double boxWidth = scanner.nextDouble();
        double boxHeight = scanner.nextDouble();
        Box box = new Box(boxLength, boxWidth, boxHeight);
        System.out.printf("The cost of the 3D box is: Rs %.2f%n", box.calCost());

        scanner.close();
    }
}
