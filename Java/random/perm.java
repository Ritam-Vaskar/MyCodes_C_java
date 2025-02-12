public class perm {
public static void permutation(String str, String newString) {

    if(str.equals("")){
        System.out.println(newString);
        return;
    }
    for(int i=0 ; i<str.length() ; i++){
        char curr = str.charAt(i);
        String left = str.substring(0, i);
        String right = str.substring(i+1);
        String comb = left + right ;
        permutation(comb, newString+curr);

    }
    
}
    


public static void main(String[] args){
    String str= "abc";
    permutation(str , "");
}

}
