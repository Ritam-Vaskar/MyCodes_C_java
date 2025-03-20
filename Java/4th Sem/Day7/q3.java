import java.io.*;
import java.util.Scanner;
//copy by byte
public class q3 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Enter the source file name: ");
        String sourceFile = scanner.nextLine();
        
        System.out.print("Enter the destination file name: ");
        String destinationFile = scanner.nextLine();

        try (FileInputStream fis = new FileInputStream(sourceFile);
             FileOutputStream fos = new FileOutputStream(destinationFile)) {

            int byteData;
            while ((byteData = fis.read()) != -1) {
                fos.write(byteData);
            }
            System.out.println("File Copied Successfully using Byte Stream.");
        } catch (IOException e) {
            System.out.println("An error occurred: " + e.getMessage());
        }

        scanner.close();
    }
}

