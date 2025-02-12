
// Write a Java class which has a method called ProcessInput(). This
// method checks the number entered by the user. If the entered number is negative then
// throw an user defined exception called NegativeNumberException, otherwise it displays
// the double value of the entered number.
// Input: Enter a number 4
// Output: Double value: 8
// Input: Enter a number -4
// Output: Caught the exception
// Exception occurred: NegativeNumberException: number should be
// positive
// package Java.4th Sem.Day6;

class NegativeNumberException extends Exception{
    public NegativeNumberException(String message){
        super(message);
    }
} 

class ProcessInput {
    public static void ProcessInput(int num){
        try{
            if(num < 0){
                throw new NegativeNumberException("number should be positive");
            }
            System.out.println("Double value: " + num*2);
        }catch(NegativeNumberException e){
            System.out.println("Caught the exception");
            System.out.println("Exception occurred: " + e);
        }
    }
   
}

public class q3 {
    public static void main(String[] args) {
        ProcessInput.ProcessInput(4);
        ProcessInput.ProcessInput(-4);
    }
}
