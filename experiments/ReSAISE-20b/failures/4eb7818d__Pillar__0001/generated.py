import json
from typing import Any, Dict

def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        Dictionary containing at least the keys:
            - 'headers': mapping of header names to values.
            - 'body'   : the raw request body (bytes or str).

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not `application/json`.
        If the body cannot be decoded as JSON.
        If the parsed payload is not a mapping (i.e., not a dict).
    """
    # Basic validation of request structure
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary.")

    headers = request.get("headers")
    body   = request.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' in request.")
    if body is None:
        raise ValueError("Missing 'body' in request.")

    # Ensure the Content-Type header indicates JSON
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not isinstance(content_type, str) or "application/json" not in content_type.lower():
        raise ValueError("Content-Type must be 'application/json'.")

    # Safely decode the body
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding failed: {exc}") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Body must be a bytes or str instance.")

    # Prevent huge payloads (CWE-693 mitigation)
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB
    if len(body_text) > MAX_BODY_SIZE:
        raise ValueError(f"Body size exceeds the maximum allowed {MAX_BODY_SIZE} bytes.")

    # Parse JSON safely
    try:
        payload = json.loads(body_text, strict=True)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decoding failed: {exc}") from exc

    # Ensure the payload is a dictionary
    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return payload