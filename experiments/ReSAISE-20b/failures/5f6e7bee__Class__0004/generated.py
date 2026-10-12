import json
from typing import Dict, Any

# Maximum allowed size for a JSON payload (1 MiB). Adjust as needed.
MAX_JSON_BODY_SIZE = 1024 * 1024  # 1,048,576 bytes


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body from a FastAPI-like dictionary.

    Parameters
    ----------
    http_request : dict
        A dictionary containing HTTP request information. It must contain at least:
            - 'headers': a dict of header names to values
            - 'body': the raw request body as bytes or str

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not 'application/json',
        if the body size exceeds MAX_JSON_BODY_SIZE,
        or if JSON decoding fails.
    """
    # Ensure headers are present
    headers = http_request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request headers are missing or malformed")

    # Retrieve the Content-Type header (case-insensitive)
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Invalid Content-Type: expected 'application/json', got '{content_type}'"
        )

    # Retrieve the body
    body = http_request.get("body")
    if body is None:
        raise ValueError("Request body is missing")

    # Normalize body to str
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body contains invalid UTF-8 bytes") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be a bytes or str object")

    # Enforce maximum size
    if len(body_str.encode("utf-8")) > MAX_JSON_BODY_SIZE:
        raise ValueError(
            f"JSON body exceeds maximum allowed size of {MAX_JSON_BODY_SIZE} bytes"
        )

    # Parse JSON safely
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    # Ensure the result is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError(f"Expected JSON object (dict), got {type(parsed).__name__}")

    return parsed