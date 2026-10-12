import json
from typing import Dict, Any


def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    input_data : dict
        Dictionary containing the request headers and body.
        Expected keys:
            - "headers": a dict of HTTP headers
            - "body": raw bytes or str containing the JSON payload

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is not 'application/json'.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = input_data.get("headers", {})
    body = input_data.get("body")

    # Validate Content-Type header
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Media Type: Expected application/json")

    # Ensure body is bytes or str
    if isinstance(body, (bytes, bytearray)):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be bytes or string")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return parsed