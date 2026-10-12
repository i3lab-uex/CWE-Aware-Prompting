import json
from typing import Dict, Any

# Maximum allowed body size in bytes (1 MB)
_MAX_BODY_SIZE = 1 * 1024 * 1024

def handle_json_request(http_request: Dict[str, Any]) -> Dict[Any, Any]:
    """
    Parse a JSON request body from an incoming FastAPI-like HTTP request.

    Parameters
    ----------
    http_request : dict
        A dictionary that must contain the keys ``headers`` and ``body``.
        ``headers`` should be a mapping of header names to values (case‑insensitive),
        and ``body`` must be a string containing the raw request payload.

    Returns
    -------
    dict
        The decoded JSON object represented as a Python dictionary.

    Raises
    ------
    ValueError
        * If the ``Content-Type`` header is missing or not exactly ``application/json``.
        * If the body exceeds :data:`_MAX_BODY_SIZE` bytes.
        * If JSON decoding fails due to malformed input.
    """
    # ---- 1. Validate headers ------------------------------------------------
    if not isinstance(http_request, dict):
        raise ValueError("Request must be a dictionary containing 'headers' and 'body'.")

    headers = http_request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' in request.")

    # Normalize header names to lower case for case‑insensitive lookup
    normalized_headers = {k.lower(): v for k, v in headers.items()}
    content_type = normalized_headers.get("content-type")

    if content_type is None:
        raise ValueError("Missing 'Content-Type' header.")
    # Strictly require application/json; ignore parameters like charset
    if not content_type.lower().startswith("application/json"):
        raise ValueError(f"Unsupported Content-Type '{content_type}'. Expected 'application/json'.")

    # ---- 2. Validate body size ---------------------------------------------
    body = http_request.get("body")
    if not isinstance(body, (str, bytes)):
        raise ValueError("Request body must be a string or bytes.")
    if isinstance(body, str):
        body_bytes = body.encode("utf-8")
    else:
        body_bytes = body

    if len(body_bytes) > _MAX_BODY_SIZE:
        raise ValueError(f"Request body too large ({len(body_bytes)} bytes). Maximum allowed is {_MAX_BODY_SIZE} bytes.")

    # ---- 3. Parse JSON ------------------------------------------------------
    try:
        decoded = json.loads(body_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from None

    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dictionary).")

    return decoded