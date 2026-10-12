import json
from typing import Dict, Any

def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        Dictionary expected to contain at least the keys 'headers' and 'body'.
        The 'headers' value should be a dict of HTTP header names to values,
        and the 'body' value should be the raw request payload as a string.

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the `Content-Type` header does not indicate JSON, or if the body
        cannot be decoded as valid JSON.
    """
    # 1. Validate presence of required keys
    if not isinstance(http_request, dict):
        raise ValueError("Request must be a dictionary.")
    headers = http_request.get("headers")
    body = http_request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")
    if body is None:
        raise ValueError("Request body is missing.")

    # 2. Validate Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not isinstance(content_type, str):
        raise ValueError("Content-Type header is missing or invalid.")
    if "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type: expected application/json")

    # 3. Ensure body is a string (FastAPI typically gives str)
    if not isinstance(body, str):
        # If body is bytes, decode it
        if isinstance(body, (bytes, bytearray)):
            try:
                body = body.decode("utf-8")
            except Exception as exc:
                raise ValueError(f"Body decoding failed: {exc}") from exc
        else:
            raise ValueError("Request body must be a string or bytes")

    # 4. Parse JSON safely
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed