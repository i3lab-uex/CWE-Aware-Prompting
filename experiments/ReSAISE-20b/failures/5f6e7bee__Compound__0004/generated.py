import json
from typing import Dict, Any


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from an HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        Dictionary containing the HTTP headers under the key ``"headers"``
        and the raw body string under the key ``"body"``.

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the `Content-Type` header is missing or does not contain
        ``application/json``.
        If the body cannot be decoded as JSON.
    """
    # Validate input structure
    if not isinstance(http_request, dict):
        raise ValueError("http_request must be a dictionary")

    headers = http_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary")

    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Ensure the request is JSON
    if "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. "
            "Expected 'application/json'."
        )

    # Retrieve body
    raw_body = http_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Body should be a string; if bytes, decode as UTF-8
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Body bytes could not be decoded as UTF-8") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes")

    # Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON body must represent an object (dictionary)")

    return parsed