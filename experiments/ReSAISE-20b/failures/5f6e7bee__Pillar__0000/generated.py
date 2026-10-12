import json
from typing import Dict, Any


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from an HTTP request represented as a dictionary.

    The function expects `http_request` to contain the keys:
        - "headers": a mapping of header names to values.
        - "body": the raw request payload as a string.

    It validates that the Content-Type header is set to 'application/json' (case‑insensitive)
    and attempts to decode the body using `json.loads`.  If either validation fails,
    a ValueError is raised with an explanatory message.

    Args:
        http_request: Dictionary containing request headers and body.

    Returns:
        A dictionary representing the parsed JSON payload.

    Raises:
        ValueError: If Content-Type is missing or not 'application/json',
                    or if the body contains invalid JSON.
    """
    # Retrieve headers, normalising keys to lowercase for case‑insensitive matching
    headers = http_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Invalid request format: 'headers' must be a dictionary")

    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        raise ValueError("Missing 'Content-Type' header")

    # Allow charset parameters (e.g., application/json; charset=utf-8)
    media_type = content_type.split(";")[0].strip().lower()
    if media_type != "application/json":
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'"
        )

    # Retrieve and validate body
    body = http_request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    if not isinstance(body, str):
        raise ValueError("Invalid request format: 'body' must be a string")

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return parsed