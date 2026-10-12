import json
from typing import Dict, Any

def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body from an incoming FastAPI request.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing the HTTP headers and body of the request.
        Expected keys:
            - "headers": dict of header names to values
            - "body": str or bytes containing the raw request body

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not application/json.
        If JSON decoding fails due to malformed data.
    """
    # Validate headers
    headers = incoming_request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request headers are missing or malformed")

    # Normalize header keys to lowercase for case-insensitive comparison
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Only accept JSON content type (allow charset param)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Retrieve body
    body = incoming_request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Ensure body is a string
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8") from exc
    elif not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    # Ensure parsed object is a dict (typical for JSON request bodies)
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return parsed