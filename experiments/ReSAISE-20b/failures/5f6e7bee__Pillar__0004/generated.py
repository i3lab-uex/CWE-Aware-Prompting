import json
from typing import Dict, Any


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like http_request dictionary.

    Args:
        http_request: A dictionary containing HTTP headers and a body string.
            Expected keys are 'headers' (dict) and 'body' (str or bytes).

    Returns:
        A dictionary representing the parsed JSON payload.

    Raises:
        ValueError: If the Content-Type header is missing or not application/json.
        ValueError: If the body cannot be decoded as valid JSON.
    """
    # Validate headers presence
    headers = http_request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request must contain 'headers' as a dictionary.")

    # Ensure Content-Type header exists and is application/json
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header.")
    # Normalize and check MIME type
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'."
        )

    # Retrieve and normalize body
    raw_body = http_request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body.")
    # Accept both str and bytes; convert bytes to str using utf-8
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Body decoding failed.") from exc
    elif not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes.")

    # Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    # Ensure the parsed object is a dictionary
    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return parsed