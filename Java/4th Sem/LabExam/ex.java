
interface Shape {
    double area();
    double perimeter();
}


class Circle implements Shape {
    private double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public double area() {
        return Math.PI * radius * radius;
    }

    @Override
    public double perimeter() {
        return 2 * Math.PI * radius;
    }
}


class Rectangle implements Shape {
    private double width;
    private double height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public double area() {
        return width * height;
    }

    @Override
    public double perimeter() {
        return 2 * (width + height);
    }
}


class ShapeCalculator {
    public void calc(Shape shape) {
        System.out.println("Area: " + shape.area());
        System.out.println("Perimeter: " + shape.perimeter());
    }
}


public class ex {
    public static void main(String[] args) {
        
        Circle circle = new Circle(5);
        Rectangle rectangle = new Rectangle(4, 6);

       
        ShapeCalculator calculator = new ShapeCalculator();

        
        calculator.calc(circle);
        calculator.calc(rectangle);
    }
}