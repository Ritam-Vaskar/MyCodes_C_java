package LeetCode;
public class sudoku {
        // Check if placing the number in the given row and column is safe
        public boolean isSafe(char[][] board, int row, int col, int number) {
            char numChar = (char) (number + '0');
            
            // Check the column
            for (int i = 0; i < board.length; i++) {
                if (board[i][col] == numChar) {
                    return false;
                }
            }
    
            // Check the row
            for (int j = 0; j < board.length; j++) {
                if (board[row][j] == numChar) {
                    return false;
                }
            }
    
            // Check the 3x3 sub-grid
            int sr = 3 * (row / 3);
            int sc = 3 * (col / 3);
    
            for (int i = sr; i < sr + 3; i++) {
                for (int j = sc; j < sc + 3; j++) {
                    if (board[i][j] == numChar) {
                        return false;
                    }
                }
            }
    
            return true;
        }
    
        // Helper function to solve the Sudoku board using backtracking
        public boolean helper(char[][] board, int row, int col) {
            if (row == board.length) {
                return true;
            }
    
            int nrow = row;
            int ncol = col + 1;
            if (col == board.length - 1) {
                nrow = row + 1;
                ncol = 0;
            }
    
            if (board[row][col] != '.') {
                return helper(board, nrow, ncol);
            } else {
                for (int i = 1; i <= 9; i++) {
                    if (isSafe(board, row, col, i)) {
                        board[row][col] = (char) (i + '0');
                        if (helper(board, nrow, ncol)) {
                            return true;
                        }
                        board[row][col] = '.';
                    }
                }
            }
    
            return false;
        }
    
        // Main function to initiate solving the Sudoku board
        public void solveSudoku(char[][] board) {
            helper(board, 0, 0);
        }
    
        public static void main(String[] args) {
            sudoku solution = new sudoku();

            //define board

            char[][] board = {
                {'5', '3', '.', '.', '7', '.', '.', '.', '.'},
                {'6', '.', '.', '1', '9', '5', '.', '.', '.'},
                {'.', '9', '8', '.', '.', '.', '.', '6', '.'},
                {'8', '.', '.', '.', '6', '.', '.', '.', '3'},
                {'4', '.', '.', '8', '.', '3', '.', '.', '1'},
                {'7', '.', '.', '.', '2', '.', '.', '.', '6'},
                {'.', '6', '.', '.', '.', '.', '2', '8', '.'},
                {'.', '.', '.', '4', '1', '9', '.', '.', '5'},
                {'.', '.', '.', '.', '8', '.', '.', '7', '9'}
            };
    
            solution.solveSudoku(board);
    
            // Print the solved board
            for (int i = 0; i < board.length; i++) {
                for (int j = 0; j < board[i].length; j++) {
                    System.out.print(board[i][j] + " ");
                }
                System.out.println();
            }
        }
    
}
