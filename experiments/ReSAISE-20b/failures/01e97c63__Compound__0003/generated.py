import json
from typing import Dict, Any

def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    client_request : dict
        Dictionary containing the HTTP request data. It must have at least two keys:
            - "headers": a dict of header names to values (case‑insensitive)
            - "body"   : the raw request body as a string or bytes

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the request body is not valid JSON.
        If the Content‑Type header does not indicate a JSON payload.

    Notes
    -----
    - Header names are treated case‑insensitively.
    - The function only parses the body; it does not enforce CSRF protection
      (that should be handled elsewhere in the request pipeline).
    """
    # Ensure required keys exist
    if "headers" not in client_request or "body" not in client_request:
        raise ValueError("Request must contain 'headers' and 'body' keys")

    headers = client_request["headers"]
    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary")

    # Normalize header names to lowercase for case‑insensitive lookup
    normalized_headers = {k.lower(): v for k, v in headers.items()}

    # Verify Content‑Type header
    content_type = normalized_headers.get("content-type", "")
    if not any(ct in content_type.lower() for ct in ("application/json", "application/ld+json")):
        raise ValueError("Content-Type must be application/json or compatible")

    # Get the raw body (bytes or str)
    raw_body = client_request["body"]
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF‑8") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes")

    # Parse JSON safely
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON") from exc

    if not isinstance(parsed, dict):
        # The function is expected to return a dictionary
        raise ValueError("JSON payload must be an object (dict)")

    return parsed