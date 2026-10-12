import json
from typing import Dict, Any

def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from an incoming HTTP request represented as a dictionary.

    Args:
        incoming_request (dict): A mapping containing at least the keys 'headers' and 'body'.
            - headers: dict of HTTP request headers (case‑insensitive).
            - body: raw request payload as a string.

    Returns:
        dict: The decoded JSON object if the request is valid.

    Raises:
        ValueError: If the Content-Type header is missing or not set to
                    application/json, or if the body cannot be parsed as JSON.
    """
    # Ensure required keys exist
    headers = incoming_request.get("headers")
    body = incoming_request.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' in the request")

    if body is None:
        raise ValueError("Missing request body")

    # Normalise header keys to lowercase for case‑insensitive lookup
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Content-Type header is missing")

    # Allow for parameters like 'application/json; charset=utf-8'
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type '{content_type}'. Expected 'application/json'")

    # Decode JSON body safely
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from None

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed