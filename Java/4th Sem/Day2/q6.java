public class q6 {
    public static void main(String[] args) {
        int arr[][]={{1,2,3},{4,5,6},{7,8,9}};
        int sum=0;
        //left digonal sum
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                if(i==j){
                    sum+=arr[i][j];
                }
            }
        }
        System.out.println(sum);

        //right digonal sum
        sum=0;
        for(int i=3;i>0;i--){
            for(int j=0;j<3;j++){
                if(i+j==2){
                    sum+=arr[i][j];
                }
            }
        }
        System.out.println(sum);
    }
}
