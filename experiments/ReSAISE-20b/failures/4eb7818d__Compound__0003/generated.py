import json
from typing import Any, Dict

# Maximum allowed size for the request body (1 MB)
MAX_BODY_SIZE = 1 * 1024 * 1024  # bytes


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    The function expects the request to be a dictionary containing at least
    the keys 'headers' and 'body'. It verifies that:
      * The `Content-Type` header is set to `application/json`.
      * A CSRF protection token is present in the headers (e.g. X-CSRF-Token).
      * The body is a string and does not exceed MAX_BODY_SIZE.
      * The body can be decoded as valid JSON.

    Parameters
    ----------
    request : dict
        Dictionary representing the incoming HTTP request. Expected keys:
            - 'headers' (dict): HTTP headers.
            - 'body'    (str or bytes): Raw request body.

    Returns
    -------
    dict
        The decoded JSON object from the request body.

    Raises
    ------
    ValueError
        If any validation step fails, a ValueError with an explanatory message
        is raised.
    """
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary.")

    headers = request.get("headers")
    body = request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")

    # Normalize header keys to lower case for case-insensitive matching
    headers_lower = {k.lower(): v for k, v in headers.items()}

    # Verify Content-Type
    content_type = headers_lower.get("content-type")
    if content_type is None or "application/json" not in content_type.lower():
        raise ValueError("Content-Type must be 'application/json'.")

    # CSRF protection: require a header X-CSRF-Token
    csrf_token = headers_lower.get("x-csrf-token")
    if not csrf_token:
        raise ValueError("Missing CSRF token in request headers.")

    # Body must be a string or bytes
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be a string or bytes.")

    # Size limit
    if len(body_str.encode("utf-8")) > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds maximum size of {MAX_BODY_SIZE} bytes.")

    # Parse JSON
    try:
        parsed_body = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    if not isinstance(parsed_body, dict):
        raise ValueError("JSON body must be an object (dictionary).")

    return parsed_body