package LabExam;
import java.util.Scanner;


class CheckPerfectNumber extends Exception {
    public CheckPerfectNumber(String message) {
        super(message);
    }
}

public class test {
    
   
    public static void checkPerfectNumber(int num) throws CheckPerfectNumber {
        if (num <= 0) {
            throw new CheckPerfectNumber("Number must be greater than zero.");
        }
        
        int sum = 0;
        for (int i = 1; i <= num / 2; i++) {
            if (num % i == 0) {
                sum += i;
            }
        }
        
        if (sum == num) {
            System.out.println(num + " is a perfect number.");
        } else {
            throw new CheckPerfectNumber(num + " is not a perfect number.");
        }
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a number: ");
        int num = scanner.nextInt();
        
        try {
            checkPerfectNumber(num);
        } catch (CheckPerfectNumber e) {
            System.out.println("Exception: " + e.getMessage());
        }
        
        scanner.close();
    }
}
