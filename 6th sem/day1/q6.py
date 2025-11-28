# Q6: Operators and Expressions

print("=== Python Operators and Expressions ===\n")

# Variables for demonstration
a = 20
b = 10
x = 5
y = 2

# Arithmetic Operators
print("--- Arithmetic Operators ---")
print(f"a = {a}, b = {b}")
print(f"Addition (+): a + b = {a + b}")
print(f"Subtraction (-): a - b = {a - b}")
print(f"Multiplication (*): a * b = {a * b}")
print(f"Division (/): a / b = {a / b}")
print(f"Floor Division (//): a // b = {a // b}")
print(f"Modulus (%): a % b = {a % b}")
print(f"Exponentiation (**): a ** b = {a ** b}")

# More examples with different numbers
print(f"\nx = {x}, y = {y}")
print(f"Division: {x} / {y} = {x / y}")
print(f"Floor Division: {x} // {y} = {x // y}")
print(f"Modulus: {x} % {y} = {x % y}")
print(f"Power: {x} ** {y} = {x ** y}")

# Complex expressions
print("\n--- Complex Expressions ---")
expr1 = (a + b) * x - y ** 2
print(f"(a + b) * x - y ** 2 = ({a} + {b}) * {x} - {y} ** 2 = {expr1}")

expr2 = a / b + x * y
print(f"a / b + x * y = {a} / {b} + {x} * {y} = {expr2}")

expr3 = (a ** 2 + b ** 2) ** 0.5  # Pythagorean theorem
print(f"√(a² + b²) = √({a}² + {b}²) = {expr3}")

# Operator Precedence (PEMDAS/BODMAS)
print("\n--- Operator Precedence ---")
result1 = 2 + 3 * 4
print(f"2 + 3 * 4 = {result1}  (Multiplication first)")

result2 = (2 + 3) * 4
print(f"(2 + 3) * 4 = {result2}  (Parentheses first)")

result3 = 10 - 5 + 3
print(f"10 - 5 + 3 = {result3}  (Left to right)")

result4 = 2 ** 3 ** 2
print(f"2 ** 3 ** 2 = {result4}  (Right to left for **)")

result5 = 10 / 2 * 5
print(f"10 / 2 * 5 = {result5}  (Left to right)")

# Comparison Operators
print("\n--- Comparison Operators ---")
print(f"a = {a}, b = {b}")
print(f"a > b: {a > b}")
print(f"a < b: {a < b}")
print(f"a >= b: {a >= b}")
print(f"a <= b: {a <= b}")
print(f"a == b: {a == b}")
print(f"a != b: {a != b}")

# Logical Operators
print("\n--- Logical Operators ---")
p = True
q = False
print(f"p = {p}, q = {q}")
print(f"p and q: {p and q}")
print(f"p or q: {p or q}")
print(f"not p: {not p}")
print(f"not q: {not q}")

# Assignment Operators
print("\n--- Assignment Operators ---")
num = 10
print(f"Initial value: num = {num}")

num += 5  # num = num + 5
print(f"After num += 5: {num}")

num -= 3  # num = num - 3
print(f"After num -= 3: {num}")

num *= 2  # num = num * 2
print(f"After num *= 2: {num}")

num /= 4  # num = num / 4
print(f"After num /= 4: {num}")

num //= 2  # num = num // 2
print(f"After num //= 2: {num}")

num %= 3  # num = num % 3
print(f"After num %= 3: {num}")

num **= 3  # num = num ** 3
print(f"After num **= 3: {num}")

# Practical Examples
print("\n--- Practical Examples ---")

# Calculate area and perimeter of rectangle
length = 15
width = 8
area = length * width
perimeter = 2 * (length + width)
print(f"Rectangle: Length={length}, Width={width}")
print(f"Area = {area}")
print(f"Perimeter = {perimeter}")

# Calculate compound interest
principal = 10000
rate = 5  # 5%
time = 3  # years
amount = principal * (1 + rate / 100) ** time
interest = amount - principal
print(f"\nCompound Interest:")
print(f"Principal: ₹{principal}")
print(f"Rate: {rate}%")
print(f"Time: {time} years")
print(f"Total Amount: ₹{amount:.2f}")
print(f"Interest Earned: ₹{interest:.2f}")

# Temperature conversion
celsius = 25
fahrenheit = (celsius * 9/5) + 32
print(f"\nTemperature Conversion:")
print(f"{celsius}°C = {fahrenheit}°F")

# Check even or odd using modulus
number = 17
is_even = (number % 2 == 0)
print(f"\nIs {number} even? {is_even}")
