
import java.io.*;

// Compare two binary files
public class q4 {
    public static void main(String[] args) {
        String file1 = "file1.bin";  
        String file2 = "file2.bin";  

        try (FileInputStream fis1 = new FileInputStream(file1);
             FileInputStream fis2 = new FileInputStream(file2)) {

            int byte1, byte2;
            int position = 0;

            while ((byte1 = fis1.read()) != -1 && (byte2 = fis2.read()) != -1) {
                position++;
                if (byte1 != byte2) {
                    System.out.println("Files differ at byte position: " + position);
                    return;
                }
            }

            if (fis1.read() == -1 && fis2.read() == -1) {
                System.out.println("Files are identical.");
            } else {
                System.out.println("Files have different lengths.");
            }

        } catch (IOException e) {
            System.out.println("An error occurred: " + e.getMessage());
        }
    }
}

