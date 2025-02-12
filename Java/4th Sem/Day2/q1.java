//find largest among three
public class q1 {
    public static void main(String[] args) {
        int a,b,c;
        // System.out.println("Enter three numbers: ");
        a = Integer.parseInt(args[0]);
        b = Integer.parseInt(args[1]);
        c = Integer.parseInt(args[2]);
        // a = new java.util.Scanner(System.in).nextInt();
        // b = new java.util.Scanner(System.in).nextInt();
        // c = new java.util.Scanner(System.in).nextInt();
        // if(a>b && a>c) System.out.println("Largest number is "+a);
        // else if(b>a && b>c) System.out.println("Largest number is "+b);
        // else System.out.println("Largest number is "+c);
        //ternary oparator
        System.out.println(a>b?(a>c?a:c):(b>c?b:c));
    }
    
}
