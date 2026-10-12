import json
from typing import Dict, Any

def validate_and_parse_json(incoming_req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that the incoming HTTP request contains a JSON body and parse it.

    Parameters
    ----------
    incoming_req : dict
        Dictionary containing the request headers and body. Expected keys:
            - "headers": a mapping of header names to values
            - "body"   : the raw request body (str or bytes)

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or not a JSON-compatible value.
        If the body cannot be decoded as valid JSON.
        If a CSRF token header is missing or empty (basic protection against
        Cross‑Site Request Forgery).
    """
    # Extract headers and body
    headers = incoming_req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")

    # Normalise header names to lowercase for case‑insensitive lookup
    hdr = {k.lower(): v for k, v in headers.items()}

    # 1. Verify Content‑Type is JSON
    content_type = hdr.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header")

    # Accept common JSON media types
    json_types = {"application/json", "application/ld+json", "application/vnd.api+json"}
    if not any(ct in content_type.lower() for ct in json_types):
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    # 2. Basic CSRF protection (requires a token header)
    csrf_token = hdr.get("x-csrf-token") or hdr.get("csrf-token")
    if not csrf_token:
        raise ValueError("Missing CSRF token header")

    # 3. Retrieve and decode the body
    raw_body = incoming_req.get("body")
    if raw_body is None:
        raise ValueError("Missing request body")

    # If bytes, decode to str
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except Exception as exc:  # pragma: no cover
            raise ValueError("Body bytes could not be decoded as UTF‑8") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Request body must be a string or bytes")

    # 4. Parse JSON
    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError("Malformed JSON in request body") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict)")

    return parsed