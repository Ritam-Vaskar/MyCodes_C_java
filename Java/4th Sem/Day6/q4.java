// Write a program to create user defined exceptions called
// HrsException, MinException and SecException. Create a class Time which contains data
// members hours, minutes, seconds and a method to take a time from user which throws
// the user defined exceptions if hours (&gt;24 &amp;&lt;0),minutes(&gt;60 &amp;&lt;0),seconds(&gt;60 &amp;&lt;0).
// Input: Enter hours: 4
// Enter minutes: 54
// Enter seconds: 34
// Output: Correct Time-&gt; 4:54:34
// Input: Enter hours: 30
// Enter minutes: 65
// Enter seconds: 65
// Output: Caught the exception
// Exception occurred: InvalidHourException:hour is not greater than 24
// Exception occurred: InvalidMinuteException:hour is not greater than 60
// Exception occurred: InvalidSecondException:hour is not greater than 60

class HrsException extends Exception{
    public HrsException(String message){
        super(message);
    }
}
class MinException extends Exception{
    public MinException(String message){
        super(message);
    }
}
class SecException extends Exception{
    public SecException(String message){
        super(message);
    }
}
class Time{
    int hours,minutes,seconds;
    void getTime() throws HrsException,MinException,SecException{
        if(hours>24 || hours<0){
            throw new HrsException("hour should not greater than 24");
        }
        if(minutes>60 || minutes<0){
            throw new MinException("hour should not greater than 60");
        }
        if(seconds>60 || seconds<0){
            throw new SecException("hour should not greater than 60");
        }
    }
}
public class q4 {
  public static void main(String[] args) {
      Time t = new Time();
      t.hours = 30;
      t.minutes = 65;
      t.seconds = 65;
      try{
          t.getTime();
      }catch(HrsException e){
          System.out.println(e.getMessage());
      }catch(MinException e){
          System.out.println(e.getMessage());
      }catch(SecException e){
          System.out.println(e.getMessage());
      }
  }
}
