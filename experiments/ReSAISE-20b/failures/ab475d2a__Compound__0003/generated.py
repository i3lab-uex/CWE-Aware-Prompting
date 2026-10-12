import json
from typing import Dict, Any

def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    req : dict
        Dictionary containing the request data. Expected keys:
            - 'headers' : mapping of header names to values
            - 'body'    : raw request body (bytes or str)

    Returns
    -------
    dict
        Parsed JSON object.

    Raises
    ------
    ValueError
        If the Content-Type is not application/json,
        if a CSRF token header is missing or invalid,
        or if the body cannot be decoded as JSON.
    """
    # ------------------------------------------------------------------
    # 1. Validate content type
    # ------------------------------------------------------------------
    headers = req.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")

    # Header names are case‑insensitive; normalize to lower‑case
    content_type = next(
        (v for k, v in headers.items() if k.lower() == "content-type"),
        None,
    )
    if content_type is None or not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type!r}. Expected 'application/json'."
        )

    # ------------------------------------------------------------------
    # 2. CSRF protection (optional but recommended)
    # ------------------------------------------------------------------
    # Some frameworks use a custom header such as X-CSRF-Token.
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token is None:
        raise ValueError("Missing CSRF token header (X-CSRF-Token).")

    # In a real application, you would validate the token against the
    # user's session or a stored value. Here we simply ensure it is present.
    if not isinstance(csrf_token, str) or not csrf_token.strip():
        raise ValueError("Invalid CSRF token value.")

    # ------------------------------------------------------------------
    # 3. Parse JSON body
    # ------------------------------------------------------------------
    raw_body = req.get("body")
    if raw_body is None:
        raise ValueError("Request body is missing.")

    # Body may be bytes or string
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Unable to decode body bytes: {exc}") from exc
    elif not isinstance(raw_body, str):
        raise ValueError(f"Body must be bytes or str, got {type(raw_body).__name__}")

    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decode error: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("Top‑level JSON element must be an object (dict).")

    return parsed