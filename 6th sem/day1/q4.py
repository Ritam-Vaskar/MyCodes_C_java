# Q4: Data Types in Python

print("=== Python Data Types ===\n")

# Integer (int)
integer_num = 42
negative_int = -15
large_int = 1000000
print("--- Integer (int) ---")
print(f"Positive Integer: {integer_num}, Type: {type(integer_num)}")
print(f"Negative Integer: {negative_int}, Type: {type(negative_int)}")
print(f"Large Integer: {large_int}, Type: {type(large_int)}")

# Float (float)
print("\n--- Float (float) ---")
float_num = 3.14
negative_float = -9.81
scientific_notation = 2.5e-3
print(f"Float Number: {float_num}, Type: {type(float_num)}")
print(f"Negative Float: {negative_float}, Type: {type(negative_float)}")
print(f"Scientific Notation: {scientific_notation}, Type: {type(scientific_notation)}")

# String (str)
print("\n--- String (str) ---")
single_quote = 'Hello'
double_quote = "World"
multiline_string = """This is a
multiline
string"""
print(f"Single Quote String: {single_quote}, Type: {type(single_quote)}")
print(f"Double Quote String: {double_quote}, Type: {type(double_quote)}")
print(f"Multiline String: {multiline_string}")
print(f"Type: {type(multiline_string)}")

# Boolean (bool)
print("\n--- Boolean (bool) ---")
is_true = True
is_false = False
comparison_result = 10 > 5
print(f"True Value: {is_true}, Type: {type(is_true)}")
print(f"False Value: {is_false}, Type: {type(is_false)}")
print(f"Comparison (10 > 5): {comparison_result}, Type: {type(comparison_result)}")

# Additional data types
print("\n--- Other Data Types ---")

# List
my_list = [1, 2, 3, "Python", True]
print(f"List: {my_list}, Type: {type(my_list)}")

# Tuple
my_tuple = (1, 2, 3, "Python")
print(f"Tuple: {my_tuple}, Type: {type(my_tuple)}")

# Dictionary
my_dict = {"name": "Alice", "age": 25, "city": "New York"}
print(f"Dictionary: {my_dict}, Type: {type(my_dict)}")

# Set
my_set = {1, 2, 3, 4, 5}
print(f"Set: {my_set}, Type: {type(my_set)}")

# None type
none_value = None
print(f"None Value: {none_value}, Type: {type(none_value)}")

# Checking data types
print("\n--- Type Checking ---")
print(f"Is integer_num an int? {isinstance(integer_num, int)}")
print(f"Is float_num a float? {isinstance(float_num, float)}")
print(f"Is single_quote a str? {isinstance(single_quote, str)}")
print(f"Is is_true a bool? {isinstance(is_true, bool)}")
