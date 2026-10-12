import json
from typing import Dict, Any

# Maximum request body size in bytes (10 MiB)
MAX_BODY_SIZE = 10 * 1024 * 1024

def handle_json_input(client_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    client_request : dict
        A dictionary that must contain a ``headers`` mapping and a ``body``
        value. The ``headers`` mapping may contain either lowercase or
        title‑case keys.

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the ``Content-Type`` header is missing or not a JSON‑compatible
        type, if the body size exceeds :data:`MAX_BODY_SIZE`, or if the
        body cannot be decoded as JSON.
    """
    # Extract headers and body
    headers = client_request.get("headers", {})
    body = client_request.get("body")

    # Resolve content‑type header case‑insensitively
    content_type = None
    for key in ("Content-Type", "content-type"):
        if key.lower() in headers:
            content_type = headers[key.lower()]
            break

    # Validate Content‑Type
    if not content_type or "application/json" not in content_type.lower():
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected application/json."
        )

    # Handle body size limit
    if isinstance(body, (bytes, bytearray)):
        body_len = len(body)
    elif isinstance(body, str):
        body_len = len(body.encode("utf-8"))
    else:
        # If the body is already a dict/list, assume it was decoded elsewhere
        if isinstance(body, (dict, list)):
            return body
        raise ValueError(f"Unsupported body type: {type(body).__name__}")

    if body_len > MAX_BODY_SIZE:
        raise ValueError(f"Request body exceeds maximum size of {MAX_BODY_SIZE} bytes")

    # Decode the body to a string if necessary
    if isinstance(body, (bytes, bytearray)):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body contains invalid UTF‑8: {exc}") from exc
    else:
        body_str = body

    # Parse JSON
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError(f"JSON payload must be an object (dict), got {type(parsed).__name__}")

    return parsed