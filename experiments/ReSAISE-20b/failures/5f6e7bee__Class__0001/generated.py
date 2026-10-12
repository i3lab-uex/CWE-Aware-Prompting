import json
from typing import Dict, Any


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the JSON body of an HTTP request represented as a dictionary.

    Parameters
    ----------
    http_request : dict
        A mapping that must contain the keys 'headers' (a mapping of header names to values)
        and 'body' (the raw request payload, expected to be a string).

    Returns
    -------
    dict
        The parsed JSON object.

    Raises
    ------
    ValueError
        If the `Content-Type` header is missing or not set to 'application/json'.
        If the request body cannot be decoded as JSON.
    """
    # Validate presence of headers and body
    if not isinstance(http_request, dict):
        raise ValueError("http_request must be a dictionary")
    headers = http_request.get("headers", {})
    body = http_request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("headers must be a dictionary")
    if body is None:
        raise ValueError("Request body is missing")

    # Normalize header names to lower case for case‑insensitive comparison
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept only application/json (case‑insensitive, ignore parameters)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # Ensure body is a string; if it's bytes, decode to UTF‑8
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF‑8") from exc
    elif not isinstance(body, str):
        raise ValueError("Request body must be a string or bytes")

    # Attempt to parse JSON
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed