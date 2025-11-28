# Q3: Input and Output Functions

print("=== Python Input and Output ===\n")

# Using print() function
print("Hello, World!")
print("Welcome to Python Programming")

# Print with multiple arguments
print("Python", "is", "awesome!", sep=" - ")

# Print with custom end character
print("This is line 1", end=" | ")
print("This is line 2")

# Formatted output using f-strings
name = "Bob"
age = 22
print(f"\nName: {name}, Age: {age}")

# Using format() method
print("Name: {}, Age: {}".format(name, age))

# Old style formatting (%)
print("\nName: %s, Age: %d" % (name, age))

print("\n" + "="*50)
print("Taking User Input")
print("="*50 + "\n")

# Getting user input
user_name = input("Enter your name: ")
user_age = input("Enter your age: ")
user_city = input("Enter your city: ")

# Displaying user input
print("\n=== User Information ===")
print(f"Name: {user_name}")
print(f"Age: {user_age}")
print(f"City: {user_city}")

# Input with type conversion
print("\n=== Input with Calculations ===")
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

sum_result = num1 + num2
print(f"\nSum of {num1} and {num2} is: {sum_result}")

# Multiple inputs in one line
print("\n=== Multiple Inputs ===")
x, y = input("Enter two numbers separated by space: ").split()
print(f"You entered: x={x}, y={y}")
