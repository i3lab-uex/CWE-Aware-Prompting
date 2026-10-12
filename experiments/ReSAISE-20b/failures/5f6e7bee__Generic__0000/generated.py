import json
from typing import Dict, Any


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        A mapping containing the HTTP headers under key 'headers' and the raw body under key 'body'.
        Expected format:
            {
                "headers": {"content-type": "application/json", ...},
                "body": '{"key":"value"}'   # or bytes
            }

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the content type is not 'application/json'.
        If the body cannot be decoded as valid JSON.
    """
    headers = http_request.get("headers", {})
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Normalize and check MIME type
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type: {content_type}. Expected 'application/json'")

    raw_body = http_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Convert bytes to str if necessary
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc

    if not isinstance(raw_body, str):
        raise ValueError(f"Body must be a string or bytes, got {type(raw_body).__name__}")

    try:
        return json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc