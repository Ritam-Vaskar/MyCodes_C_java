// // C Program to demonstrate array initialization
// #include <stdio.h>
 
// int main()
// {
 
//     // array initialization using initialier list
//     int arr[5] = { 10, 20, 30, 40, 50 };
 
//     // array initialization using initializer list without
//     // specifying size
//     int arr1[] = { 1, 2, 3, 4, 5 };
 
//     // array initialization using for loop
//     float arr2[5];
//     for (int i = 0; i < 5; i++) {
//         arr2[i] = (float)i * 2.1;
//     }
//     return 0;
// }






// // C Program to illustrate element access using array
// // subscript
// #include <stdio.h>

// int main()
// {

// 	// array declaration and initialization
// 	int arr[5] = { 15, 25, 35, 45, 55 };

// 	// accessing element at index 2 i.e 3rd element
// 	printf("Element at arr[2]: %d\n", arr[2]);

// 	// accessing element at index 4 i.e last element
// 	printf("Element at arr[4]: %d\n", arr[4]);

// 	// accessing element at index 0 i.e first element
// 	printf("Element at arr[0]: %d", arr[0]);

// 	return 0;
// }




// // C Program to demonstrate the use of array
// #include <stdio.h>

// int main()
// {
// 	// array declaration and initialization
// 	int arr[5] = { 10, 20, 30, 40, 50 };

// 	// modifying element at index 2
// 	arr[2] = 100;

// 	// traversing array using for loop
// printf("Elements in Array: ");
// 	for (int i = 0; i < 5; i++) {
// 		printf("%d ", arr[i]);
// 	}

// 	return 0;
// }




// // C Program to calculate size of an array using sizeof()
// // operator
// #include <stdio.h>
 
// int main()
// {
 
//     int Arr[] = { 1, 2, 3, 4, 5 };
   
//     // variable to store size of Arr
//     int length = sizeof(Arr) / sizeof(Arr[0]);
 
//     printf("The length of the array is: %d\n", length);
 
//     return 0;
// }

