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
    }
}