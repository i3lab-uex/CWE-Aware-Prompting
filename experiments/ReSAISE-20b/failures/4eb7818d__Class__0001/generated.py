import json
from typing import Any, Dict


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        The request object containing at least the keys:
        - "headers": a mapping of HTTP headers.
        - "body"   : the raw request body (bytes or str).

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type is not application/json,
        if JSON decoding fails, or if the request body
        cannot be processed.
    """
    # Basic checks for required keys
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary.")
    headers = request.get("headers")
    body = request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary.")
    if body is None:
        raise ValueError("Missing request body.")

    # Verify Content-Type header
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Unsupported Content-Type. Expected application/json.")

    # Ensure body is bytes or string
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to decode request body bytes: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:  # pragma: no cover
        raise ValueError("Request body must be bytes or string.")

    # Prevent excessively large payloads (e.g., >10 MB)
    MAX_BODY_SIZE = 10 * 1024 * 1024
    if len(body_str.encode("utf-8")) > MAX_BODY_SIZE:
        raise ValueError("Request body exceeds maximum allowed size.")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed