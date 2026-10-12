import json
from typing import Dict, Any


def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body from an incoming FastAPI request.

    Parameters
    ----------
    incoming_request : dict
        A dictionary containing the HTTP headers and body of the incoming request.
        Expected keys are:
            - "headers": a dict mapping header names to values
            - "body": the raw request body as a string or bytes

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or does not contain 'application/json'.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = incoming_request.get("headers", {})
    body = incoming_request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Normalize header keys to lowercase for case‑insensitive lookup
    normalized_headers = {k.lower(): v for k, v in headers.items()}

    content_type = normalized_headers.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Incorrect content type: expected 'application/json'")

    if body is None:
        raise ValueError("Request body is missing")

    # Ensure body is a string for json.loads
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body decoding error: body is not valid UTF‑8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON") from exc

    if not isinstance(parsed, dict):
        # FastAPI normally expects a JSON object for request bodies
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed