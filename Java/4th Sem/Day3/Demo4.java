// Write a program to overload subtract method with various
// parameters in a class in Java. Write the driver class to use the different subtract
// methods using object.
// Input: Mention various subtract method having different parameters.
// Output: Subtract method will display the result accordingly

class SubtractOverload {
    public int subtract(int a, int b) {
        return a - b;
    }
    public int subtract(int a, int b, int c) {
        return a - b - c;
    }

}
public class Demo4 {
    public static void main(String[] args) {
        SubtractOverload so = new SubtractOverload();
        System.out.println("Subtracting two integers: " + so.subtract(10, 5));
        
        System.out.println("Subtracting three integers: " + so.subtract(10, 5, 2));
        
    }
}
