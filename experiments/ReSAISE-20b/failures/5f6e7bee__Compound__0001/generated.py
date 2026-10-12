import json
from typing import Dict, Any

def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of a FastAPI request.

    Parameters
    ----------
    http_request : dict
        A dictionary containing the HTTP headers and body of the incoming request.
        Expected keys:
            - "headers": dict[str, str]
            - "body": str

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not 'application/json'.
        If the JSON body cannot be decoded.
    """
    # Validate headers
    headers = http_request.get("headers", {})
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")
    # Normalize media type (ignore parameters like charset)
    mime_type = content_type.split(";")[0].strip().lower()
    if mime_type != "application/json":
        raise ValueError(f"Unsupported Content-Type: '{content_type}'. Expected 'application/json'.")

    # Retrieve body
    body = http_request.get("body")
    if body is None:
        raise ValueError("Missing request body.")
    if not isinstance(body, str):
        raise ValueError(f"Request body must be a string, got {type(body).__name__}.")

    # Parse JSON
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from None

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return payload