import json
from typing import Dict, Any

MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB limit for safety


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from an HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        Dictionary containing the HTTP headers and body. Expected keys:
            - 'headers': dict of request headers
            - 'body'   : str or bytes containing the raw body

    Returns
    -------
    dict
        Parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not `application/json`.
        If the body size exceeds ``MAX_BODY_SIZE``.
        If JSON decoding fails due to malformed data or encoding issues.
    """
    # 1. Validate headers
    headers = http_request.get("headers", {})
    content_type = headers.get("Content-Type") or headers.get("content-type")

    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")
    # Accept only exact application/json or with charset
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: '{content_type}'. Expected 'application/json'."
        )

    # 2. Retrieve body
    raw_body = http_request.get("body")
    if raw_body is None:
        raise ValueError("Request body is missing.")

    # 3. Ensure body is bytes or string
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding failed: {exc}") from exc
    elif not isinstance(raw_body, str):
        raise ValueError(f"Body must be a string or bytes, got {type(raw_body).__name__}.")

    # 4. Enforce size limit
    if len(raw_body) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds maximum size of {MAX_BODY_SIZE} bytes.")

    # 5. Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc.msg} at line {exc.lineno} column {exc.colno}") from exc

    # 6. Ensure the top-level is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed