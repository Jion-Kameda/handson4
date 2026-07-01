import json
import logging
from typing import Optional, Tuple

import azure.functions as func

from calculator import divide, multiply, normalize_number

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def _json_response(payload: dict, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json",
    )


def _error_response(message: str, status_code: int = 400) -> func.HttpResponse:
    return _json_response({"error": message}, status_code=status_code)


def _parse_operands(req: func.HttpRequest) -> Tuple[Optional[float], Optional[float], Optional[func.HttpResponse]]:
    raw_a = req.params.get("A")
    raw_b = req.params.get("B")

    if raw_a is None or raw_b is None:
        return None, None, _error_response("Query parameters 'A' and 'B' are required.", 400)

    try:
        a = float(raw_a)
        b = float(raw_b)
    except ValueError:
        return None, None, _error_response("Query parameters 'A' and 'B' must be numeric.", 400)

    return a, b, None


@app.route(route="multiply", methods=["GET"])
def multiply_api(req: func.HttpRequest) -> func.HttpResponse:
    try:
        a, b, error = _parse_operands(req)
        if error:
            return error

        result = normalize_number(multiply(a, b))
        return _json_response({"operation": "multiply", "a": normalize_number(a), "b": normalize_number(b), "result": result})
    except Exception:
        logging.exception("Unexpected error in multiply API.")
        return _error_response("Internal server error.", 500)


@app.route(route="divide", methods=["GET"])
def divide_api(req: func.HttpRequest) -> func.HttpResponse:
    try:
        a, b, error = _parse_operands(req)
        if error:
            return error

        if b == 0:
            return _error_response("Division by zero is not allowed.", 400)

        result = normalize_number(divide(a, b))
        return _json_response({"operation": "divide", "a": normalize_number(a), "b": normalize_number(b), "result": result})
    except Exception:
        logging.exception("Unexpected error in divide API.")
        return _error_response("Internal server error.", 500)
