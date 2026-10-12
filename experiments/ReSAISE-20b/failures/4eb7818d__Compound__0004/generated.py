import json
from typing import Dict, Any

# Maximum allowed body size in bytes (e.g., 1 MB)
MAX_BODY_SIZE = 1_048_576

# CSRF token header name
CSRF_HEADER = "X-CSRF-Token"


def parse_json_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        A dictionary representing the HTTP request. Expected keys:
            - "headers" : dict of header names to values (case‑insensitive)
            - "body"    : raw body bytes or string

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the Content‑Type header is missing or not `application/json`.
        If a CSRF token header is expected but missing.
        If the body exceeds ``MAX_BODY_SIZE``.
        If JSON decoding fails or the parsed value is not a dict.
    """
    # ---- 1. Validate headers -------------------------------------------------
    headers = request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")

    # Normalize header names to lower case for case‑insensitive lookup
    headers = {k.lower(): v for k, v in headers.items()}

    content_type = headers.get("content-type", "")
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            "Unsupported Content-Type. Expected 'application/json' "
            f"but got '{content_type}'."
        )

    # CSRF protection: ensure the token header is present
    if CSRF_HEADER.lower() not in headers:
        raise ValueError(f"Missing CSRF token header '{CSRF_HEADER}'")

    # ---- 2. Validate body size ---------------------------------------------
    raw_body = request.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # Accept bytes or str; convert to bytes for size check
    if isinstance(raw_body, str):
        raw_bytes = raw_body.encode("utf-8")
    elif isinstance(raw_body, bytes):
        raw_bytes = raw_body
    else:
        raise ValueError("Request body must be bytes or string")

    if len(raw_bytes) > MAX_BODY_SIZE:
        raise ValueError("Request body too large")

    # ---- 3. Decode JSON ------------------------------------------------------
    try:
        decoded = json.loads(raw_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    # Ensure the decoded value is a dict
    if not isinstance(decoded, dict):
        raise ValueError("JSON payload must be an object (dictionary)")

    # ---- 4. Return ------------------------------------------------------------
    return decoded