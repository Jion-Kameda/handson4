def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    return a / b


def normalize_number(value: float):
    #引数がfloat型であり、小数点以下が0の場合はint型に変換する
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value
