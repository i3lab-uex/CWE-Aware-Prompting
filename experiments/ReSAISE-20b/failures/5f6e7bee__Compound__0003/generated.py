import json
from typing import Dict, Any

def handle_json_request(http_request: Dict[str, Any]) -> Dict:
    """
    Parse a JSON request body from an HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        A dictionary that contains at least two keys:
            - 'headers': a mapping of header names to values.
            - 'body': the raw request body as a string or bytes.

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not JSON,
        or if the body cannot be decoded as valid JSON.
    """
    # Retrieve headers and body
    headers = http_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Normalize header keys to lowercase for case‑insensitive lookup
    headers_lc = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lc.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept only application/json or compatible media types
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    body = http_request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Ensure body is a string for json.loads
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8") from exc

    if not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed