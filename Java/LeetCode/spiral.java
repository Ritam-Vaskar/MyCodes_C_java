package Java.LeetCode;

public class spiral {
    public static int[] spiralOrder(int[][] matrix) {
       int minrow = 0;
       int mincol = 0;
       int maxrow = matrix.length - 1;
       int maxcol = matrix[0].length - 1;
       int size = matrix.length * matrix[0].length;
       int count = 0;
       while (count < size) {
           //top row
           for (int i = mincol; i <= maxcol  ; i++) {
               System.out.print(matrix[minrow][i] + " ");
               count++;
           }
           minrow++;
           //right column
           for (int i = minrow; i <= maxrow  ; i++) {
               System.out.print(matrix[i][maxcol] + " ");
               count++;
           }
           maxcol--;
           //bottom row
           for (int i = maxcol; i >= mincol  ; i--) {
               System.out.print(matrix[maxrow][i] + " ");
               count++;
           }
           maxrow--;
           //left column
           for (int i = maxrow; i >= minrow  ; i--) {
               System.out.print(matrix[i][mincol] + " ");
               count++;
           }
           mincol++;

        
       }
    }
    //spiral matrix
    public static void main(String[] args) {
        int[][] matrix = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        
        int[] result = spiralOrder(matrix);
        for (int num : result) {
            System.out.print(num + " ");
        }
    }
}