import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class OracleJDBC {
    public static void main(String[] args) {
        // Oracle Database Connection URL
        String url = "jdbc:oracle:thin:@localhost:1521:xe"; // Change 'xe' to your DB name if different
        String user = "system"; // Your Oracle username
        String password = "kiit"; // Your Oracle password

        try {
            // Load Oracle JDBC Driver
            Class.forName("oracle.jdbc.driver.OracleDriver");

            // Establish the connection
            Connection conn = DriverManager.getConnection(url, user, password);
            System.out.println("Connected to Oracle Database!");

            // Close connection
            conn.close();
        } catch (ClassNotFoundException e) {
            System.out.println("Oracle JDBC Driver not found.");
            e.printStackTrace();
        } catch (SQLException e) {
            System.out.println("Connection failed!");
            e.printStackTrace();
        }
    }
}
