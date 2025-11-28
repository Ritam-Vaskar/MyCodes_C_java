# Q2: Comments in Python

# This is a single-line comment
# Comments are used to explain code and improve readability

"""
This is a multi-line comment (docstring)
It can span multiple lines
Used for documentation purposes
"""

# Variable declarations with comments
name = "Alice"  # Inline comment: stores user's name
age = 25        # Inline comment: stores user's age

# Function with comments
def calculate_area(length, width):
    """
    Calculate the area of a rectangle.
    
    Args:
        length: Length of the rectangle
        width: Width of the rectangle
    
    Returns:
        Area of the rectangle
    """
    # Formula: Area = length * width
    area = length * width
    return area

# Main program
print("=== Comments Demonstration ===")
print(f"Name: {name}")
print(f"Age: {age}")

# Calculate and display area
rectangle_length = 10  # in meters
rectangle_width = 5    # in meters
result = calculate_area(rectangle_length, rectangle_width)
print(f"\nArea of rectangle: {result} square meters")

# TODO: Add more features later
# FIXME: Check for negative values

"""
Best Practices for Comments:
1. Write clear and concise comments
2. Avoid obvious comments
3. Update comments when code changes
4. Use comments to explain WHY, not WHAT
5. Use docstrings for functions and classes
"""
