package LeetCode;
class issort {
    public boolean check(int[] nums) {
        int count = 0;  
        int n = nums.length;

        for (int i = 0; i < n; i++) {
            if (nums[i] > nums[(i + 1) % n]) {
                count++;
            }
        }
        
        return count <= 1; 
    }

    // Main method for testing
    public static void main(String[] args) {
        Solution sol = new Solution();
        int[] nums1 = {3, 4, 5, 1, 2}; // True
        int[] nums2 = {2, 1, 3, 4}; // False
        int[] nums3 = {1, 2, 3, 4, 5}; // True
        int[] nums4 = {1, 1, 1, 1}; // True (All elements same)
        int[] nums5 = {6, 10, 6}; // True

        System.out.println(sol.check(nums1)); // Output: true
        System.out.println(sol.check(nums2)); // Output: false
        System.out.println(sol.check(nums3)); // Output: true
        System.out.println(sol.check(nums4)); // Output: true
        System.out.println(sol.check(nums5)); // Output: false
    }
}
