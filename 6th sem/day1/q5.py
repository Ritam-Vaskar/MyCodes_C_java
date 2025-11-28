# Q5: Number Operations and Type Conversion

print("=== Number Operations and Type Conversion ===\n")

# Basic number operations
num1 = 10
num2 = 3
float_num = 5.5

print("--- Basic Operations ---")
print(f"Addition: {num1} + {num2} = {num1 + num2}")
print(f"Subtraction: {num1} - {num2} = {num1 - num2}")
print(f"Multiplication: {num1} * {num2} = {num1 * num2}")
print(f"Division: {num1} / {num2} = {num1 / num2}")
print(f"Floor Division: {num1} // {num2} = {num1 // num2}")
print(f"Modulus: {num1} % {num2} = {num1 % num2}")
print(f"Exponentiation: {num1} ** {num2} = {num1 ** num2}")

# Mixed operations (int and float)
print("\n--- Mixed Operations (int and float) ---")
result1 = num1 + float_num
print(f"Int + Float: {num1} + {float_num} = {result1}, Type: {type(result1)}")

result2 = num1 * float_num
print(f"Int * Float: {num1} * {float_num} = {result2}, Type: {type(result2)}")

# Type Conversion (Explicit)
print("\n--- Type Conversion (Casting) ---")

# int to float
int_val = 25
float_val = float(int_val)
print(f"int to float: {int_val} -> {float_val}, Type: {type(float_val)}")

# float to int (truncates decimal)
float_val2 = 9.99
int_val2 = int(float_val2)
print(f"float to int: {float_val2} -> {int_val2}, Type: {type(int_val2)}")

# string to int
str_num = "123"
int_from_str = int(str_num)
print(f"str to int: '{str_num}' -> {int_from_str}, Type: {type(int_from_str)}")

# string to float
str_float = "45.67"
float_from_str = float(str_float)
print(f"str to float: '{str_float}' -> {float_from_str}, Type: {type(float_from_str)}")

# int to string
num_to_str = str(100)
print(f"int to str: 100 -> '{num_to_str}', Type: {type(num_to_str)}")

# float to string
float_to_str = str(3.14)
print(f"float to str: 3.14 -> '{float_to_str}', Type: {type(float_to_str)}")

# bool to int
bool_val = True
int_from_bool = int(bool_val)
print(f"bool to int: {bool_val} -> {int_from_bool}")

bool_val2 = False
int_from_bool2 = int(bool_val2)
print(f"bool to int: {bool_val2} -> {int_from_bool2}")

# Implicit Type Conversion (Type Coercion)
print("\n--- Implicit Type Conversion ---")
x = 10      # int
y = 5.5     # float
z = x + y   # Python automatically converts x to float
print(f"{x} (int) + {y} (float) = {z} (float)")
print(f"Result type: {type(z)}")

# Advanced number functions
print("\n--- Built-in Number Functions ---")
numbers = [5, -3, 8, -12, 15, 2]
print(f"Numbers: {numbers}")
print(f"abs(-10): {abs(-10)}")  # Absolute value
print(f"pow(2, 3): {pow(2, 3)}")  # Power
print(f"round(3.7): {round(3.7)}")  # Rounding
print(f"max(numbers): {max(numbers)}")  # Maximum
print(f"min(numbers): {min(numbers)}")  # Minimum
print(f"sum(numbers): {sum(numbers)}")  # Sum

# User input with type conversion
print("\n--- User Input with Type Conversion ---")
user_input = input("Enter a number: ")
print(f"Input as string: '{user_input}', Type: {type(user_input)}")

converted_num = float(user_input)
print(f"Converted to float: {converted_num}, Type: {type(converted_num)}")

# Calculation with user input
doubled = converted_num * 2
print(f"Your number doubled: {doubled}")
