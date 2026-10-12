import json
from typing import Dict, Any

def process_json_payload(req_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON payload from an HTTP request.

    Parameters
    ----------
    req_data : dict
        Dictionary that includes both the headers and body of the HTTP request.
        Expected keys are:
            - 'headers': a mapping of header names to values
            - 'body'   : the raw request body (bytes or str)

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not a JSON-compatible value.
        If the body cannot be decoded as valid JSON.
    """
    # Extract headers and body, allowing for missing keys
    headers = req_data.get("headers", {})
    raw_body = req_data.get("body")

    if raw_body is None:
        raise ValueError("Request body is missing.")

    # Normalize header names to lowercase for case‑insensitive lookup
    content_type = None
    for key, value in headers.items():
        if key.lower() == "content-type":
            content_type = value
            break

    # Validate Content-Type header
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError("Content-Type must be application/json")

    # Decode body if it's bytes
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body is not valid UTF‑8") from exc

    # Parse JSON with strict mode (default) to avoid unsafe types
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON") from exc

    # Ensure the top‑level object is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object")

    return parsed