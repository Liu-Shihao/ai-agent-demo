import math


def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b


def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b


def sin(a: float) -> float:
    """Take the sine of a number."""
    return math.sin(a)


def cos(a: float) -> float:
    """Take the cosine of a number."""
    return math.cos(a)


def radians(a: float) -> float:
    """Convert degrees to radians."""
    return math.radians(a)


def exponentiation(a: float, b: float) -> float:
    """Raise one number to the power of another."""
    return a ** b


def sqrt(a: float) -> float:
    """Take the square root of a number."""
    return math.sqrt(a)


def ceil(a: float) -> float:
    """Round a number up to the nearest integer."""
    return math.ceil(a)
