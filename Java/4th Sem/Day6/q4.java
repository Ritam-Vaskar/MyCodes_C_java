import java.util.Scanner;


class HrsException extends Exception {
    public HrsException(String message) {
        super(message);
    }
}


class MinException extends Exception {
    public MinException(String message) {
        super(message);
    }
}


class SecException extends Exception {
    public SecException(String message) {
        super(message);
    }
}


class Time {
    int hours, minutes, seconds;

    
    void validateTime() throws HrsException, MinException, SecException {
        boolean errorOccurred = false;

        
        if (hours > 24 || hours < 0) {
            System.out.println("Exception occurred: InvalidHourException: hour is not greater than 24");
            errorOccurred = true;
        }

        
        if (minutes > 60 || minutes < 0) {
            System.out.println("Exception occurred: InvalidMinuteException: minute is not greater than 60");
            errorOccurred = true;
        }

      
        if (seconds > 60 || seconds < 0) {
            System.out.println("Exception occurred: InvalidSecondException: second is not greater than 60");
            errorOccurred = true;
        }

        
        if (!errorOccurred) {
            System.out.println("Correct Time -> " + hours + ":" + minutes + ":" + seconds);
        }
    }
}


public class q4 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        
        System.out.print("Enter hours: ");
        int hours = scanner.nextInt();
        System.out.print("Enter minutes: ");
        int minutes = scanner.nextInt();
        System.out.print("Enter seconds: ");
        int seconds = scanner.nextInt();
        
        scanner.close();

       
        Time t = new Time();
        t.hours = hours;
        t.minutes = minutes;
        t.seconds = seconds;

        try {
            t.validateTime();
        } catch (HrsException | MinException | SecException e) {
            System.out.println("Caught the exception");
            System.out.println("Exception occurred: " + e.getMessage());
        }
    }
}
