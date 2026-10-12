import json
from typing import Dict, Any

# Maximum allowed size for a JSON body (in bytes). Adjust as needed.
_MAX_JSON_BODY_SIZE = 2 * 1024 * 1024  # 2 MB


def handle_json_request(http_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON request body from a FastAPI-style HTTP request dictionary.

    Parameters
    ----------
    http_request : dict
        Dictionary containing the request headers under the key 'headers'
        and the raw body content under the key 'body'.  The headers
        dictionary should map header names to values, case‑insensitively.

    Returns
    -------
    dict
        The decoded JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the Content‑Type header is missing or not a JSON media type.
        If the body exceeds :data:`_MAX_JSON_BODY_SIZE`.
        If the body cannot be decoded as valid JSON.
    """
    # 1. Validate presence of headers and body
    if not isinstance(http_request, dict):
        raise ValueError("http_request must be a dictionary")
    headers = http_request.get("headers", {})
    body = http_request.get("body")

    if not isinstance(headers, dict):
        raise ValueError("'headers' must be a dictionary")
    if body is None:
        raise ValueError("Request body is missing")

    # 2. Normalise header names to lowercase for case‑insensitive lookup
    lower_headers = {k.lower(): v for k, v in headers.items()}
    content_type = lower_headers.get("content-type")

    # 3. Validate Content‑Type
    if content_type is None:
        raise ValueError("Missing 'Content-Type' header")
    # Accept common JSON media types
    if not any(ct in content_type.lower() for ct in ("application/json", "text/json")):
        raise ValueError(f"Unsupported content type: {content_type}")

    # 4. Validate body size
    if isinstance(body, (bytes, bytearray)):
        body_bytes = bytes(body)
    else:
        # Assume string; encode to UTF‑8 for size check
        body_bytes = str(body).encode("utf-8")

    if len(body_bytes) > _MAX_JSON_BODY_SIZE:
        raise ValueError("Request body too large")

    # 5. Decode JSON
    try:
        decoded = json.loads(body_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    # 6. Ensure the result is a dictionary
    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    return decoded