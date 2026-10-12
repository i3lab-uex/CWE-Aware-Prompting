import json
from typing import Dict, Any

def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        The incoming request object. Expected to contain a 'body' key
        with raw bytes or string data.

    Returns
    -------
    dict
        The decoded JSON payload as a dictionary.

    Raises
    ------
    ValueError
        If the body is missing, not a string/bytes, or cannot be decoded as JSON.
    """
    # Ensure the request contains a body
    if 'body' not in request:
        raise ValueError("Request missing 'body' field")

    body = request['body']

    # Body must be bytes or str; if bytes, decode as UTF-8
    if isinstance(body, bytes):
        try:
            body = body.decode('utf-8')
        except Exception as exc:
            raise ValueError(f"Failed to decode request body bytes: {exc}") from exc
    elif not isinstance(body, str):
        raise ValueError(f"Unsupported body type: {type(body).__name__}")

    # Optionally enforce a maximum size to mitigate large payload attacks
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB
    if len(body) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds maximum allowed size of {MAX_BODY_SIZE} bytes")

    # Parse JSON with strict validation
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decoding failed: {exc.msg}") from exc

    # Ensure the decoded payload is a dictionary
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at top level, got {type(payload).__name__}")

    return payload