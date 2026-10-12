import json
from typing import Dict, Any

# Define a simple CSRF token key that the application expects.
CSRF_HEADER = "X-CSRF-Token"


def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    The function performs the following checks:
        1. Ensures that the `Content-Type` header is set to `application/json`
           (case‑insensitive, ignoring any charset parameters).
        2. Verifies that a CSRF token header is present to mitigate
           Cross‑Site Request Forgery attacks.
        3. Attempts to decode the request body as JSON and returns it
           as a Python dictionary.

    Parameters
    ----------
    input_data : dict
        A mapping containing at least two keys:
            - ``headers``: a dictionary of request headers.
            - ``body``   : the raw request body (bytes or str).

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the `Content-Type` header is missing or not JSON.
        If a CSRF token header is missing (optional but recommended).
        If the body cannot be decoded as JSON.
    """
    # --- 1. Validate headers -------------------------------------------------
    if not isinstance(input_data, dict):
        raise ValueError("input_data must be a dictionary")

    headers = input_data.get("headers")
    body = input_data.get("body")

    if not isinstance(headers, dict):
        raise ValueError("headers must be a dictionary")
    if body is None:
        raise ValueError("body is missing from input_data")

    # Normalize header names to lower-case for case‑insensitive lookup
    headers_lower = {k.lower(): v for k, v in headers.items()}

    # Check Content-Type
    content_type = headers_lower.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. "
            "Expected 'application/json'."
        )

    # Optional CSRF protection: ensure a token header is present
    if CSRF_HEADER.lower() not in headers_lower:
        raise ValueError(
            f"Missing required header '{CSRF_HEADER}'. "
            "This request may be vulnerable to CSRF."
        )

    # --- 2. Decode JSON body -----------------------------------------------
    try:
        if isinstance(body, bytes):
            # FastAPI typically provides a bytes object for raw bodies
            body_text = body.decode("utf-8")
        else:
            body_text = str(body)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to decode body as UTF-8: {exc}") from exc

    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError(
            f"JSON payload must be an object (dict), got {type(parsed).__name__}"
        )

    return parsed