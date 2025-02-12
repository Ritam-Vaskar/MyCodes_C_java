import java.util.Scanner;

class Plate {
    protected double length;
    protected double width;

    public Plate(double length, double width) {
        this.length = length;
        this.width = width;
        System.out.println("Plate constructor called");
        System.out.println("Dimensions - Length: " + length + ", Width: " + width);
    }
}

class Box extends Plate {
    protected double height;

    public Box(double length, double width, double height) {
        super(length, width);
        this.height = height;
        System.out.println("Box constructor called");
        System.out.println("Height: " + height);
    }
}

class WoodBox extends Box {
    private double thickness;

    public WoodBox(double length, double width, double height, double thickness) {
        super(length, width, height);
        this.thickness = thickness;
        System.out.println("WoodBox constructor called");
        System.out.println("Thickness: " + thickness);
    }

    public void dis() {
        System.out.println("\nFinal Dimensions:");
        System.out.println("Length: " + length);
        System.out.println("Width: " + width);
        System.out.println("Height: " + height);
        System.out.println("Thickness: " + thickness);
    }
}

public class q2 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter length: ");
        double length = scanner.nextDouble();
        System.out.print("Enter width: ");
        double width = scanner.nextDouble();
        System.out.print("Enter height: ");
        double height = scanner.nextDouble();
        System.out.print("Enter thickness: ");
        double thickness = scanner.nextDouble();

        WoodBox Box = new WoodBox(length, width, height, thickness);
        Box.dis();

        scanner.close();
    }
}
