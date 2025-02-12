package dummy;
class Pen{
    String color;
    String type; //ballpoint;gel

    public void Write(){
        System.out.println("Writing something");
    }
}
public class random{
    public static void main(String args[]){
        Pen pen1 = new Pen();
        pen1.color = "blue";
        pen1.type = "gel";

        pen1.Write();
    }
}