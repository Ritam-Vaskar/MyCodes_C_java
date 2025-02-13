// Create an user defined exception named CheckArgument to check
// the number of arguments passed through command line. If the number of arguments is
// less than four then throw the Check Argument exception, else print the addition of squares
// of all the four elements.
// Input: 4 3 2 1
// Output : 30
// Input: 4 3 2
// Output : Exception occurred - CheckArgument
// package Java.4th Sem.Day6;

// User-defined exception class
import java.util.Scanner;

class CheckArgument extends Exception {
    CheckArgument(String message) {
        super(message);
    }
}

public class q5 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        try {
            System.out.print("Enter 4 integers: ");
            String[] input = sc.nextLine().split(" ");

            if (input.length < 4) {
                throw new CheckArgument("Exception occurred - CheckArgument");
            }

            int sum = 0;
            for (String numStr : input) {
                int num = Integer.parseInt(numStr);
                sum += num * num;
            }

            System.out.println("Output: " + sum);
        } catch (CheckArgument e) {
            System.out.println(e.getMessage());
        } catch (NumberFormatException e) {
            System.out.println("Invalid input! Please enter only integers.");
        } finally {
            sc.close();
        }
    }
}