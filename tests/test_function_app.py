import json
from pathlib import Path
import sys

import azure.functions as func
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FUNCTION_APP_DIR = PROJECT_ROOT / "src" / "function_app"
if str(FUNCTION_APP_DIR) not in sys.path:
    sys.path.insert(0, str(FUNCTION_APP_DIR))

from function_app import divide_api, multiply_api


def _make_request(params: dict[str, str]) -> func.HttpRequest:
    return func.HttpRequest(
        method="GET",
        url="http://localhost/api/test",
        params=params,
        body=b"",
    )


def _response_json(response: func.HttpResponse) -> dict:
    return json.loads(response.get_body().decode("utf-8"))


def test_multiply_api_returns_result() -> None:
    response = multiply_api(_make_request({"A": "6", "B": "7"}))

    assert response.status_code == 200
    body = _response_json(response)
    assert body["operation"] == "multiply"
    assert body["a"] == 6
    assert body["b"] == 7
    assert body["result"] == 42


def test_divide_api_returns_result() -> None:
    response = divide_api(_make_request({"A": "10", "B": "4"}))

    assert response.status_code == 200
    body = _response_json(response)
    assert body["operation"] == "divide"
    assert body["a"] == 10
    assert body["b"] == 4
    assert body["result"] == 2.5


@pytest.mark.parametrize(
    "params",
    [
        {"A": "1"},
        {"B": "2"},
        {},
    ],
)
def test_multiply_api_returns_400_when_query_params_are_missing(params: dict[str, str]) -> None:
    response = multiply_api(_make_request(params))

    assert response.status_code == 400
    body = _response_json(response)
    assert "error" in body
    assert body["error"] == "Query parameters 'A' and 'B' are required."


def test_divide_api_returns_400_when_non_numeric_parameter_is_given() -> None:
    response = divide_api(_make_request({"A": "abc", "B": "2"}))

    assert response.status_code == 400
    body = _response_json(response)
    assert "error" in body
    assert body["error"] == "Query parameters 'A' and 'B' must be numeric."


def test_divide_api_returns_400_when_dividing_by_zero() -> None:
    response = divide_api(_make_request({"A": "10", "B": "0"}))

    assert response.status_code == 400
    body = _response_json(response)
    assert "error" in body
    assert body["error"] == "Division by zero is not allowed."
