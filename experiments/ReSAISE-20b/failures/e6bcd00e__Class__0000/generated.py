import json
from typing import Dict, Any


def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like incoming_request dictionary.

    Parameters
    ----------
    incoming_request : dict
        A dictionary containing the HTTP headers and body of the incoming request.
        Expected keys:
            - "headers": dict
                Mapping of header names to values. Header names are case-insensitive.
            - "body": str or bytes
                The raw request body.

    Returns
    -------
    dict
        Parsed JSON object as a dictionary.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not application/json.
        If JSON decoding fails due to malformed data.
    """
    # Extract headers and body
    headers = incoming_request.get("headers", {})
    raw_body = incoming_request.get("body")

    if raw_body is None:
        raise ValueError("Missing request body")

    # Normalise header keys to lowercase for case-insensitive lookup
    headers_lower = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lower.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Only accept application/json, optionally with charset
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Decode body to string if it is bytes
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    # Ensure the result is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed