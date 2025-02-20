// -Write a program to perform following operations on user entered strings and
// a character –
// i) Change the case of the string
// ii) Reverse the string
// iii) Compare two strings
// iv) Insert one string into another string
// v) Convert the string to upper case and lower case
// vi) Check whether the character is present in the string and at which position
// vii) Check whether the string is palindrome or not.
// viii) Check the number of word, vowel and consonant in the string

import java.util.Scanner;

public class q1 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a string: ");
        String str = scanner.nextLine();

        System.out.print("Enter a character: ");
        char ch = scanner.next().charAt(0);

        System.out.println("1. Change the case of the string");
        System.out.println("2. Reverse the string");
        System.out.println("3. Compare two strings");
        System.out.println("4. Insert one string into another string");
        System.out.println("5. Convert the string to upper case and lower case");
        System.out.println("6. Check whether the character is present in the string and at which position");
        System.out.println("7. Check whether the string is palindrome or not");
        System.out.println("8. Check the number of word, vowel and consonant in the string");
        System.out.print("Enter your choice: ");
        int choice = scanner.nextInt();

        switch (choice) {
            case 1:
                System.out.println("1. Change the case of the string");
                System.out.println("1. Uppercase");
                System.out.println("2. Lowercase");
                System.out.print("Enter your choice: ");
                int caseChoice = scanner.nextInt();

                switch (caseChoice) {
                    case 1:
                        System.out.println("Uppercase: " + str.toUpperCase());
                        break;
                    case 2:
                        System.out.println("Lowercase: " + str.toLowerCase());
                        break;
                    default:
                        System.out.println("Invalid choice!");
                        break;
                }
                break;
            case 2:
                System.out.println("2. Reverse the string");
                StringBuilder reversedStr = new StringBuilder(str).reverse();
                System.out.println("Reversed string: " + reversedStr);
                break;
            case 3:
                System.out.println("3. Compare two strings");
                System.out.print("Enter another string: ");
                scanner.nextLine();
                String str2 = scanner.nextLine();
                System.out.println("Comparison: " + str.compareTo(str2));
                break;
            case 4:
                System.out.println("4. Insert one string into another string");
                System.out.print("Enter the index to insert the character: ");
                int index = scanner.nextInt();
                System.out.print("Enter the string to insert: ");
                scanner.nextLine();
                String insertStr = scanner.nextLine();
                StringBuilder strBuilder = new StringBuilder(str);
                strBuilder.insert(index, insertStr);
                System.out.println("Inserted string: " + strBuilder);
                break;
            case 5:
                System.out.println("5. Convert the string to upper case and lower case");
                System.out.println("Uppercase: " + str.toUpperCase());
                System.out.println("Lowercase: " + str.toLowerCase());
                break;
            case 6:
                System.out.println("6. Che  ck whether the character is present in the string and at which position");
                if (str.indexOf(ch) != -1) {
                    System.out.println("Character is present at position: " + (str.indexOf(ch) + 1));
                } else {
                    System.out.println("Character is not present in the string");
                }
                break;
            case 7: 
                System.out.println("7. Check whether the string is palindrome or not");
                if (str.equals(new StringBuilder(str).reverse().toString())) {
                    System.out.println("String is palindrome");
                } else {
                    System.out.println("String is not palindrome");
                }
                break;
            case 8:
                System.out.println("8. Check the number of word, vowel and consonant in the string");
                int wordCount = 1;
                int vowelCount = 0;
                int consonantCount = 0;
                for (int i = 0; i < str.length(); i++) {
                    if (str.charAt(i) == ' ') {
                        wordCount++;
                    } else if (str.charAt(i) >= 'A' && str.charAt(i) <= 'Z') {
                        vowelCount++;
                    } else if (str.charAt(i) >= 'a' && str.charAt(i) <= 'z') {
                        consonantCount++;
                    }
                }
                System.out.println("Number of words: " + wordCount);
                System.out.println("Number of vowels: " + vowelCount);
                System.out.println("Number of consonants: " + consonantCount);
                break;
            default:
                System.out.println("Invalid choice!");
                break;
        }
    }
}