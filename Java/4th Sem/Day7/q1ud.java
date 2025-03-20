public class q1ud {

    public static boolean compareStrings(String str1, String str2) {
        if (str1.length() != str2.length()) {
          return false;
        }
    
        for (int i = 0; i < str1.length(); i++) {
          if (str1.charAt(i) != str2.charAt(i)) {
            return false;
          }
        }
    
        return true;
      }


    
    public static void main(String[] args) {
        String str = "Hello World";
        System.out.println("Original String: " + str);
    
        // uppercase
        String upperCaseStr = "";
        for (int i = 0; i < str.length(); i++) {
          char c = str.charAt(i);
          if (c >= 'a' && c <= 'z') {
            upperCaseStr += (char) (c - 32); 
          } else {
            upperCaseStr += c;
          }
        }
        System.out.println("Uppercase String: " + upperCaseStr);
    
        // lowercase
        String lowerCaseStr = "";
        for (int i = 0; i < str.length(); i++) {
          char c = str.charAt(i);
          if (c >= 'A' && c <= 'Z') {
            lowerCaseStr += (char) (c + 32); 
          } else {
            lowerCaseStr += c;
          }
        }
        System.out.println("Lowercase String: " + lowerCaseStr);

        // Reverse
        String reversedStr = ""; 
        for (int i=str.length()-1; i>=0; i--) {
            reversedStr += str.charAt(i);
        }
        System.out.println("Reversed String: " + reversedStr);
        
        //compare
        String str1 = "Hello";
        String str2 = "Hello";
        if (compareStrings(str1, str2)) {
            System.out.println("Strings are equal");
        } else {
            System.out.println("Strings are not equal");
        }

        // Check whether the character is present in the string and at which position without built-in functions
        char ch = 'o';
        int index = -1;
        for (int i = 0; i < str.length(); i++) {
            if (str.charAt(i) == ch) {
                index = i;
                break;
            }
        }
        if (index != -1) {
            System.out.println("Character '" + ch + "' is present at index " + index);
        } else {
            System.out.println("Character '" + ch + "' is not present in the string");
        }

        // Check whether the string is palindrome or not. without build in functions
        boolean isPalindrome = true;
        for (int i = 0; i < str.length() / 2; i++) {
            if (str.charAt(i) != str.charAt(str.length() - 1 - i)) {
                isPalindrome = false;
                break;
            }
        }
        if (isPalindrome) {
            System.out.println("The string is a palindrome.");
        } else {
            System.out.println("The string is not a palindrome.");
        }

        // Check the number of word, vowel and consonant in the string without built-in functions
        int wordCount = 1;
        int vowelCount = 0;
        int consonantCount = 0;
        for (int i = 0; i < str.length(); i++) {
            if (str.charAt(i) == ' ') {
                wordCount++;
            } else if (str.charAt(i) == 'a' || str.charAt(i) == 'e' || str.charAt(i) == 'i' || str.charAt(i) == 'o' || str.charAt(i) == 'u') {
                vowelCount++;
            } else {
                consonantCount++;
            }
        }
        System.out.println("Number of words: " + wordCount);
        System.out.println("Number of vowels: " + vowelCount);
        System.out.println("Number of consonants: " + consonantCount);

    }
}