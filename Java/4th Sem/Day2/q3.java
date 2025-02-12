public class q3 {
    public static void main(String[] args) {
        int arr[]={15,20,13,24,53,6,71,8,39,10};
        for(int i=0;i<9;i++){
            for(int j=i+1;j<10;j++){
                if(arr[i]>arr[j]){
                    int temp=arr[i];
                    arr[i]=arr[j];
                    arr[j]=temp;
                }
            }
        }
        for(int i=0;i<10;i++){
            System.out.print(arr[i]);
            System.out.print(" ");
        }
    }
    
}