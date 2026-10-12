import json
from typing import Dict, Any

# Maximum allowed request body size (1 MiB)
MAX_BODY_SIZE = 1 << 20  # 1,048,576 bytes


def handle_json_request(http_request: Dict[str, Any]) -> Dict:
    """
    Parse a JSON request body from an HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        Dictionary containing the HTTP headers and body. Expected keys are
        'headers' (a dict) and 'body' (bytes or str).

    Returns
    -------
    dict
        Parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is not ``application/json``.
        If the body is missing, empty or exceeds :data:`MAX_BODY_SIZE`.
        If JSON decoding fails due to malformed input.
    """
    # Retrieve headers (case‑insensitive lookup)
    headers = http_request.get("headers", {})
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if content_type is None or "application/json" not in content_type.lower():
        raise ValueError("Invalid content type, expected application/json")

    # Retrieve and validate body
    body = http_request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Ensure the body is bytes or str
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be bytes or str")

    # Enforce size limit
    if len(body_str.encode("utf-8")) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds maximum allowed size of {MAX_BODY_SIZE} bytes")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON payload") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON root must be an object (dictionary)")

    return parsed