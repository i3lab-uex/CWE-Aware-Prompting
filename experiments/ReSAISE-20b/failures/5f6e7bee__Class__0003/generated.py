import json
from typing import Dict, Any

def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from an HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        Dictionary containing at least the keys 'headers' and 'body'.
        The headers value is expected to be a mapping of header names
        to values. The body should be a string or bytes containing the
        raw JSON payload.

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the 'Content-Type' header is missing or not set to a JSON
        media type, or if the body cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = http_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Normalize header names to lowercase for case-insensitive lookup
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = str(value).lower()
            break

    if not content_type or "application/json" not in content_type:
        raise ValueError("Content-Type must be application/json")

    body = http_request.get("body")
    if body is None:
        raise ValueError("Request body is missing")

    # Accept both str and bytes; decode bytes to string using utf-8
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Body bytes could not be decoded as UTF-8") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed