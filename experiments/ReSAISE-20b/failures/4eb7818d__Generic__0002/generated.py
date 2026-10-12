import json
from typing import Any, Dict

MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB limit for request bodies


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        Dictionary containing at least the keys:
            - 'headers': mapping of header names to values.
            - 'body': raw request body (bytes or str).

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the body cannot be decoded as JSON or if other processing issues arise.
    """
    # Basic sanity checks
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary")

    headers = request.get("headers", {})
    body = request.get("body")

    if body is None:
        raise ValueError("Missing request body")

    # Ensure headers are a mapping
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Check content type
    content_type = headers.get("Content-Type", "").lower()
    if "application/json" not in content_type:
        raise ValueError("Unsupported Content-Type; expected application/json")

    # Limit body size for security
    if isinstance(body, bytes):
        body_len = len(body)
    elif isinstance(body, str):
        body_len = len(body.encode("utf-8"))
    else:
        raise ValueError("Body must be bytes or str")

    if body_len > MAX_BODY_SIZE:
        raise ValueError("Request body too large")

    # Decode bytes to string if necessary
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc
    else:
        body_text = body

    # Parse JSON
    try:
        payload = json.loads(body_text, strict=True)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    # Ensure payload is a dictionary
    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return payload