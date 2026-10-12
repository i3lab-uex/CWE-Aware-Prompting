import json
from typing import Dict, Any

def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a FastAPI request body expecting JSON content.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing the HTTP headers and body of the request.
        Expected keys:
            - "headers": dict with header names as keys (case-insensitive)
            - "body": str or bytes containing the raw request body

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not JSON.
        If the body cannot be decoded as valid JSON.
    """
    # 1. Validate headers
    headers = incoming_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Invalid headers format; expected a dictionary.")

    # Header names are case-insensitive
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected 'application/json'."
        )

    # 2. Retrieve and validate body
    raw_body = incoming_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body.")

    # Ensure the body is a string or bytes; if bytes, decode as UTF-8
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8.") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes.")

    # 3. Decode JSON
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return payload