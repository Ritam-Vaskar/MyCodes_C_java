// public class q3 {
//     public static void main(String[] args) {
//     int arr[] = new int[10];
//     int odd=0 , even=0;
//     for (int i = 0; i < 10; i++) {
//         if(i%2==0){
//             even++;
//         }
//         else{
//             odd++;
//         }
//     }
//     System.out.println("Number of even numbers: "+even);
//     System.out.println("Number of odd numbers: "+odd);
    
// }

class q2 {
    public static void main(String[] args) {
        int[ ] list = new int[10];
        for(int i = 0; i < list.length; i++) {
            list[i] = Integer.parseInt(args[i]);
        }
        
        System.out.print("The array : ");
        for(int i : list) {
            System.out.print(i + " ");
        }

        System.out.print("\nThe odd numbers : ");
        for(int i : list) {
            if(i % 2 != 0) {
            System.out.print(i + " ");
            }
        }

        System.out.print("\nThe even numbers : ");
        for(int i : list) {
            if(i % 2 == 0) {
                System.out.print(i + " ");
            }
        }
    }
}