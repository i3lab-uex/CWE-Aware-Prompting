import json
from typing import Any, Dict

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req_data : dict
        A dictionary containing at least the request headers and body.
        Expected keys:
            - 'headers': a mapping of header names to values
            - 'body'   : the raw request body as bytes or string

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not acceptable.
        If the body cannot be decoded as valid JSON.
    """
    # Retrieve headers and body
    headers = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Normalise header names to lowercase for case‑insensitive lookup
    headers_lower = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lower.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept only JSON media types
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Retrieve body
    raw_body = req_data.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Ensure the body is a string before parsing
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body contains invalid UTF‑8 bytes") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes")

    # Parse JSON safely
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return payload