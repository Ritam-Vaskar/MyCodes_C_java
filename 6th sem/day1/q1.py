# Q1: Variables, Identifiers, Constants and Literals

# Declaring variables with meaningful identifiers
student_name = "John Doe"
student_age = 20
student_grade = 85.5
is_passed = True

# Constants (by convention, use UPPERCASE)
MAX_MARKS = 100
PI = 3.14159
COLLEGE_NAME = "ABC College"

# Different types of literals
integer_literal = 42
float_literal = 3.14
string_literal = "Hello, Python!"
boolean_literal = True
none_literal = None

# Displaying values
print("=== Variables and Identifiers ===")
print(f"Student Name: {student_name}")
print(f"Student Age: {student_age}")
print(f"Student Grade: {student_grade}")
print(f"Is Passed: {is_passed}")

print("\n=== Constants ===")
print(f"Maximum Marks: {MAX_MARKS}")
print(f"Value of PI: {PI}")
print(f"College Name: {COLLEGE_NAME}")

print("\n=== Literals ===")
print(f"Integer Literal: {integer_literal}")
print(f"Float Literal: {float_literal}")
print(f"String Literal: {string_literal}")
print(f"Boolean Literal: {boolean_literal}")
print(f"None Literal: {none_literal}")

# Multiple assignment
x, y, z = 10, 20, 30
print(f"\nMultiple Assignment: x={x}, y={y}, z={z}")

# Same value to multiple variables
a = b = c = 100
print(f"Same value assignment: a={a}, b={b}, c={c}")
