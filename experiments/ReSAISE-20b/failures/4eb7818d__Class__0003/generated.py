import json
from typing import Dict, Any

def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        Dictionary representing the incoming HTTP request. Expected keys:
            - "headers": dict of HTTP headers
            - "body"   : raw request body (bytes or str)

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the request is missing required fields, or if JSON decoding fails,
        or if the parsed body is not a dictionary.
    """
    # Basic sanity checks
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary")

    headers = request.get("headers")
    body = request.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' field")

    if body is None:
        raise ValueError("Missing request body")

    # Ensure the content type indicates JSON
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type; expected application/json")

    # Decode bytes to string if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Body bytes could not be decoded as UTF-8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes")

    # Enforce a reasonable size limit (e.g., 1 MB)
    MAX_BODY_SIZE = 1 * 1024 * 1024
    if len(body_str) > MAX_BODY_SIZE:
        raise ValueError("Request body exceeds maximum allowed size")

    # Parse JSON safely
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    # Ensure the parsed data is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed