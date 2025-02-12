

// -Define an interface Motor with a data member –capacity and two methods
// such as run() and consume(). Define a Java class ‘Washing machine’ which implements this
// interface and write the code to check the value of the interface data member thru an object of the
// class.

// Input - mentioned in the program
// Output - Capacity of the motor is -----

interface Motor {
    int capacity = 1000;
    public void run();
    public void consume();
    
}

class WashingMachine implements Motor {
    // public static void main(String[] args) {
    //     WashingMachine obj = new WashingMachine();
    //     System.out.println("Capacity of the motor is " + obj.capacity);
    // }
    @Override
    public void run() {
        System.out.println("Running");
    }
    @Override
    public void consume() {
        System.out.println("Consuming");
    }
    void display() {
        System.out.println("Capacity of the motor is " + capacity);
    }
}
public class q2 {
    public static void main(String[] args) {
        WashingMachine obj = new WashingMachine();
        obj.run();
        obj.consume();
        obj.display();
    }
    
}
