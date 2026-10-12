import json
from typing import Dict, Any

def analyze_json_request(incoming_request: Dict[str, Any]) -> Dict:
    """
    Parse a JSON request body from an incoming FastAPI-like request dictionary.

    Parameters
    ----------
    incoming_request : dict
        Dictionary expected to contain the HTTP request data with keys:
            - 'headers' : mapping of header names to values.
            - 'body'    : raw request body (bytes or str).

    Returns
    -------
    dict
        The decoded JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not 'application/json'.
        If a CSRF token header is expected but missing.
        If the body cannot be decoded as valid JSON.
    """
    # --- Header validation -------------------------------------------------
    headers = incoming_request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    # Normalize header names to lowercase for case‑insensitive comparison
    normalized_headers = {k.lower(): v for k, v in headers.items()}

    content_type = normalized_headers.get("content-type")
    if content_type is None:
        raise ValueError("Missing 'Content-Type' header")

    # Only accept application/json (allow optional charset)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. Expected 'application/json'"
        )

    # --- Optional CSRF protection -----------------------------------------
    # Some applications may require a custom header to mitigate CSRF.
    # Uncomment the following lines if you want to enforce it.

    # csrf_token = normalized_headers.get("x-csrf-token")
    # if not csrf_token:
    #     raise ValueError("Missing CSRF token header 'X-CSRF-Token'")

    # --- Body decoding ----------------------------------------------------
    body = incoming_request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # FastAPI typically provides the body as bytes; decode if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding failed: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be bytes or str")

    # Parse JSON safely
    try:
        payload = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return payload