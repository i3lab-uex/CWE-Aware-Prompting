import json
from typing import Dict, Any


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-like HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        Dictionary containing at least the keys 'headers' and 'body'.
        `headers` should be a mapping of header names to values.
        `body` is expected to be a string containing the raw request payload.

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or does not indicate JSON,
        if the body is missing, or if the body contains malformed JSON.
    """
    # Basic validation of input structure
    if not isinstance(http_request, dict):
        raise ValueError("http_request must be a dictionary")

    headers = http_request.get("headers")
    body = http_request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("headers must be a dictionary")
    if body is None:
        raise ValueError("Missing request body")

    # Normalize header keys to lowercase for case‑insensitive comparison
    content_type = headers.get("content-type") or headers.get("Content-Type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Ensure the request claims to be JSON
    if "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type '{content_type}'. Expected 'application/json'"
        )

    # Limit the size of the body to prevent DoS attacks
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 MB
    if isinstance(body, str) and len(body.encode("utf-8")) > MAX_BODY_SIZE:
        raise ValueError("Request body exceeds maximum allowed size")

    # Parse the JSON payload
    try:
        decoded = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc

    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return decoded