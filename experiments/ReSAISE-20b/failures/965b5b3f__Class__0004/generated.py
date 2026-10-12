import json
from typing import Any, Dict

def process_json_request(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req_data : dict
        Dictionary containing at least the keys 'headers' and 'body'.
        - `req_data['headers']` should be a mapping of header names to values.
        - `req_data['body']` should be the raw request body as a string or bytes.

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the `Content-Type` header does not indicate JSON.
        If the body is empty or cannot be decoded as valid JSON.
    """
    # Extract headers and body
    headers = req_data.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary.")

    # Normalize header names to lowercase for case-insensitive lookup
    headers_lower = {k.lower(): v for k, v in headers.items()}

    content_type = headers_lower.get("content-type", "")
    # Accept common JSON media types
    if not any(ct in content_type.lower() for ct in ("application/json", "text/json")):
        raise ValueError(f"Unsupported Content-Type: '{content_type}'. Expected application/json.")

    body = req_data.get("body")
    if body is None:
        raise ValueError("Request body is missing.")

    # Ensure the body is a string (decode bytes if necessary)
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc

    if not isinstance(body, str):
        raise ValueError("Body must be a string or bytes.")

    body = body.strip()
    if not body:
        raise ValueError("Request body is empty.")

    # Parse JSON safely
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return payload