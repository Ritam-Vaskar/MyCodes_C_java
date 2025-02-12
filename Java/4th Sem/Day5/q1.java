
// An abstract class ‘student’ with two data members roll no, reg no, a method getinput() and an abstract
// method course() A subclass ‘kiitian’ with course() method implementation
// Write the driver class to print the all details of a kiitian object.

// Input - Rollno - 2205180

// Registration no - 1234567890

// Output -Rollno - 2205180

// Registration no - 1234567890
// Course - B.Tech. (Computer Science &amp; Engg)

abstract class student {
    int rollNo, regNo;
    public void getinput(int rollNo, int regNo) {
        this.rollNo = rollNo;
        this.regNo = regNo;
        System.out.println("Rollno - " + rollNo);
        System.out.println("Registration no - " + regNo);
    }
    public abstract void course();
}

class kiitian extends student {
    public void course() {
        System.out.println("Course - B.Tech. (Computer Science &amp; Engg)");
    }
}
public class q1 {
    public static void main(String[] args) {
        kiitian k = new kiitian();
        k.getinput(2205180,1234567890);
        k.course();

    }
    
}
