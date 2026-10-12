import json
from typing import Dict, Any

# Maximum body size in bytes (e.g., 1 MB) to mitigate large payload attacks
MAX_BODY_SIZE = 1 * 1024 * 1024  # 1 MB


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        A dictionary representing the incoming HTTP request. Expected keys:
            - 'headers': a mapping of header names to values.
            - 'body': the raw request body, either as bytes or str.

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the request lacks required fields, if the Content-Type is not JSON,
        or if JSON decoding fails. Also raised for oversized bodies.
    """
    # Basic request structure validation
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary.")

    headers = request.get("headers")
    body = request.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Request missing 'headers' dictionary.")

    if body is None:
        raise ValueError("Request missing 'body' field.")

    # Enforce Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not isinstance(content_type, str) or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type; expected application/json.")

    # Prevent excessively large payloads
    if isinstance(body, bytes):
        body_len = len(body)
        if body_len > MAX_BODY_SIZE:
            raise ValueError(f"Request body exceeds maximum size of {MAX_BODY_SIZE} bytes.")
        body_text = body.decode("utf-8")
    elif isinstance(body, str):
        if len(body.encode("utf-8")) > MAX_BODY_SIZE:
            raise ValueError(f"Request body exceeds maximum size of {MAX_BODY_SIZE} bytes.")
        body_text = body
    else:
        raise ValueError("Request 'body' must be bytes or str.")

    # Parse JSON safely
    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decoding failed: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed