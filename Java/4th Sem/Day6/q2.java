// Write a Java program to handle an ArithmeticException using try,
// catch, and finally block.
// Input: Operand values for division operation mentioned in the program
// Output: ArithmeticException caught by try-catch-finally block

// package Java.4th Sem.Day6;

public class q2 {
    public static void main(String[] args) {
        int dividend = 10;
        int divisor = 0;

        try {
            int quotient = dividend / divisor;
            System.out.println("Quotient: " + quotient);
        } catch (ArithmeticException e) {
            System.out.println("ArithmeticException caught: " + e.getMessage());
        } finally {
            System.out.println("Finally block executed");
        }
    }
}
