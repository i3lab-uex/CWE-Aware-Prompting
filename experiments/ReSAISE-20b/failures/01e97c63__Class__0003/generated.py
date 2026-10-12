import json
from typing import Dict, Any

def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    client_request : dict
        Dictionary containing the HTTP request headers and body.
        Expected keys:
            - "headers": dict of header names to values
            - "body": str or bytes containing the request payload

    Returns
    -------
    dict
        The parsed JSON content.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not a JSON-compatible type.
        If the request body cannot be parsed as valid JSON.
    """
    # Extract headers and body
    headers = client_request.get("headers", {})
    body = client_request.get("body")

    if body is None:
        raise ValueError("Request body is missing.")

    # Ensure body is a string
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body contains invalid UTF-8 bytes.") from exc
    elif not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes.")

    # Check Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Accept common JSON media types
    if not any(ct in content_type.lower() for ct in ("application/json", "application/ld+json",
                                                    "application/vnd.api+json")):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body.") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed