// Write a Java program to generate an
// ArrayIndexOutofBoundsException and handle it using catch statement.
// Input: Enter the numbers -Example: 1 2 3 4 5 ( Suppose array size is 4 )
// Output: Exception in thread “main” java.lang.ArrayIndexOutOfBoundsException:4
import java.util.Scanner;

// public class q1 {
//     public static void main(String[] args) {
//         Scanner scanner = new Scanner(System.in);
//         System.out.print("Enter the numbers: ");
//         String[] input = scanner.nextLine().split(" ");

//         int[] num = new int[4]; 
//         try{
//             for(int i=0 ; i<5 ; i++){
//                 num[i] = 
//             }
//         }

//         scanner.close();
//     }
// }

import java.util.Scanner;

public class q1 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the numbers: ");
        String[] input = scanner.nextLine().split(" ");

        int[] numbers = new int[4]; 

        try {
            for (int i = 0; i < input.length; i++) {
                numbers[i] = Integer.valueOf(input[i]);
            }
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Exception caught: " + e.getMessage());
        }

        scanner.close();
    }
}
