from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FUNCTION_APP_DIR = PROJECT_ROOT / "src" / "function_app"
if str(FUNCTION_APP_DIR) not in sys.path:
    sys.path.insert(0, str(FUNCTION_APP_DIR))

from calculator import divide, multiply, normalize_number


def test_multiply_returns_expected_value() -> None:
    assert multiply(6, 7) == 42


def test_divide_returns_expected_value() -> None:
    assert divide(10, 4) == 2.5


def test_normalize_number_converts_integer_float_to_int() -> None:
    assert normalize_number(5.0) == 5
    assert isinstance(normalize_number(5.0), int)


def test_normalize_number_keeps_fraction_float() -> None:
    assert normalize_number(5.25) == 5.25
    assert isinstance(normalize_number(5.25), float)
