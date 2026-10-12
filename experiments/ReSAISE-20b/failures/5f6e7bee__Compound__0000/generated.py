import json
from typing import Dict, Any


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like http_request dictionary.

    Parameters
    ----------
    http_request : dict
        Dictionary containing the HTTP headers and body of an incoming request.
        Expected keys:
            - "headers": dict of header names to values (case-insensitive).
            - "body": raw request body as bytes or str.

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type is not application/json or if JSON decoding fails.
    """
    # Extract headers and body
    try:
        headers = http_request["headers"]
        raw_body = http_request["body"]
    except KeyError as exc:
        raise ValueError(f"Missing expected key in http_request: {exc}") from None

    # Normalise header keys to lowercase for case‑insensitive lookup
    headers_lower = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lower.get("content-type", "")
    if "application/json" not in content_type.lower():
        raise ValueError(f"Invalid Content-Type: expected application/json, got '{content_type}'")

    # Ensure body is text; if bytes, decode using UTF‑8
    if isinstance(raw_body, bytes):
        try:
            body_text = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF‑8: {exc}") from None
    elif isinstance(raw_body, str):
        body_text = raw_body
    else:
        raise ValueError(f"Unsupported body type: {type(raw_body).__name__}")

    # Parse JSON
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from None

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed