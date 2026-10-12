import json
from typing import Dict, Any

def validate_json_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    input_data : dict
        A dictionary containing at least the keys 'headers' and 'body'.
        ``input_data['headers']`` should be a mapping of header names to values.
        ``input_data['body']`` is expected to be the raw request body (bytes or str).

    Returns
    -------
    dict
        The decoded JSON payload as a Python dictionary.

    Raises
    ------
    ValueError
        If the Content-Type header is missing or does not indicate JSON.
        If a CSRF‑related security check fails (e.g. missing X-CSRF-Token).
        If the body cannot be decoded as valid JSON.
    """
    # ------------------------------------------------------------------
    # 1. Validate Content-Type
    # ------------------------------------------------------------------
    headers = input_data.get("headers", {})
    content_type = headers.get("Content-Type") or headers.get("content-type")

    if not content_type:
        raise ValueError("Missing Content-Type header.")

    # Accept common JSON media types
    if "application/json" not in content_type.lower():
        raise ValueError(f"Unsupported Content-Type '{content_type}'. Expected 'application/json'.")

    # ------------------------------------------------------------------
    # 2. Basic CSRF protection (simple header check)
    # ------------------------------------------------------------------
    # In a real application you would validate a CSRF token against the
    # user's session or a signed cookie. Here we merely ensure that the
    # header exists to illustrate awareness of the issue.
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token is None:
        raise ValueError("Missing CSRF token header (X-CSRF-Token).")

    # ------------------------------------------------------------------
    # 3. Decode JSON body
    # ------------------------------------------------------------------
    raw_body = input_data.get("body")
    if raw_body is None:
        raise ValueError("Missing request body.")

    # Convert bytes to str if necessary
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body is not valid UTF-8: {exc}") from exc

    if not isinstance(raw_body, str):
        raise ValueError("Body must be a string or bytes.")

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return payload