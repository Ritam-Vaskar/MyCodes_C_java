// Create an user defined exception named CheckArgument to check
// the number of arguments passed through command line. If the number of arguments is
// less than four then throw the Check Argument exception, else print the addition of squares
// of all the four elements.
// Input: 4 3 2 1
// Output : 30
// Input: 4 3 2
// Output : Exception occurred - CheckArgument
package Java.4th Sem.Day6;

public class q5 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the numbers: ");
        int num1 = scanner.nextInt();
        int num2 = scanner.nextInt();
        int num3 = scanner.nextInt();
        int num4 = scanner.nextInt();

        try {
            if (args.length < 4) {
                throw new CheckArgument("Exception occurred - CheckArgument");
            }
            int sum = num1 * num1 + num2 * num2 + num3 * num3 + num4 * num4;
            System.out.println("Sum of squares: " + sum);
        } catch (CheckArgument e) {
            System.out.println(e.getMessage());
        }

        scanner.close();
    }
}
