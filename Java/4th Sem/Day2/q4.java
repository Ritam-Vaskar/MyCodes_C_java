// Program to find no. of objects created out of a class using
// ‘static’ modifier.
// Input: No of objects created
// Output: Display the number of objects created (e.g. no of objects=3)

public class q4 {
    private static int count = 0;

    public q4() {
        count++;
    }

    public static int getNumberOfObjects() {
        return count;
    }

    public static void main(String[] args) {
        System.out.println("Enter the number of objects to create:");
        java.util.Scanner scanner = new java.util.Scanner(System.in);
        int n = scanner.nextInt();

        for (int i = 0; i < n; i++) {
            q4 obj = new q4();
        }

        System.out.println("Number of objects created: " + q4.getNumberOfObjects());
    }
}
