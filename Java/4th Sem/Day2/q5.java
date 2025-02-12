import java.util.Scanner;

public class q5 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int arr[] = new int[10];
        int count = 0;

        System.out.println("Enter 10 numbers:");
        for (int i = 0; i < 10; i++) {
            arr[i] = scanner.nextInt();
        }

        
        System.out.println("Enter a number to count occurances of:");
        int num = scanner.nextInt();

        for (int i = 0; i < 10; i++) {
            if (arr[i] == num) {
                count++;
            }
        }

        System.out.println("Number of occurances of " + num + " is " + count);
    }
}