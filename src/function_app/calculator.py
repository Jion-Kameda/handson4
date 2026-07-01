def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    return a / b


def normalize_number(value: float):
    # Keep response values compact for browser readability (e.g., 5 instead of 5.0).
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value
