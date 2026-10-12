import json
from typing import Dict, Any


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from an HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        A dictionary that must contain at least two keys:
            * 'headers' – a mapping of HTTP header names to values
            * 'body'    – the raw request body (str or bytes)

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the request does not contain a JSON body, if the Content-Type header is missing or incorrect,
        or if the JSON payload cannot be decoded.
    """
    # Extract headers, normalising key names to lower-case for case‑insensitive comparison
    headers = http_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Invalid request: headers must be a dictionary")

    # Determine content type; treat missing header as error
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Allow only application/json; ignore charset or parameters
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. Expected application/json"
        )

    # Retrieve the body
    raw_body = http_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Ensure the body is a string; if bytes, decode using UTF‑8
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes")

    # Security: guard against excessively large payloads
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB
    if len(raw_body) > MAX_BODY_SIZE:
        raise ValueError("Request body is too large")

    # Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed