import java.io.*;
import java.util.Scanner;
//file statistics
public class q5 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        
        System.out.print("Enter the name of the file: ");
        String filename = scanner.nextLine();

        int charCount = 0, wordCount = 0, lineCount = 0;

        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;

            while ((line = reader.readLine()) != null) {
                lineCount++;  
                charCount += line.length(); 
                wordCount += line.split("\\s+").length;  
            }

            System.out.println("No. of characters: " + charCount);
            System.out.println("No. of lines: " + lineCount);
            System.out.println("No. of words: " + wordCount);

        } catch (IOException e) {
            System.out.println("An error occurred: " + e.getMessage());
        }

        scanner.close();
    }
}
