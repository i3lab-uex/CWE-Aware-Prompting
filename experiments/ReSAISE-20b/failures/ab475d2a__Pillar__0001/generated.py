import json
from typing import Dict, Any

def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req : dict
        Dictionary representing the incoming request. It must contain:
            - 'headers': a mapping of header names to values.
            - 'body': the raw request body (bytes or str).

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or does not indicate JSON.
        If the body cannot be decoded as valid JSON.
    """
    # Ensure headers exist
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary.")

    headers = req.get('headers')
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    # Normalize header names to lowercase for case-insensitive lookup
    content_type = headers.get('Content-Type') or headers.get('content-type')
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Accept common JSON media types
    if not any(ct in content_type.lower() for ct in ('application/json', 'text/json')):
        raise ValueError("Unsupported Content-Type. Expected application/json.")

    # Retrieve body
    body = req.get('body')
    if body is None:
        raise ValueError("Missing request body.")

    # Ensure body is a string for json.loads
    if isinstance(body, bytes):
        try:
            body_str = body.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Body contains invalid UTF‑8.") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be bytes or str.")

    # Optional: guard against excessively large payloads
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB
    if len(body_str) > MAX_BODY_SIZE:
        raise ValueError("Body size exceeds the maximum allowed limit.")

    try:
        decoded = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return decoded