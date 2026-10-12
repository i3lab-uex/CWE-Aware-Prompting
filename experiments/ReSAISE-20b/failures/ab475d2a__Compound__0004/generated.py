import json
from typing import Dict, Any

def decode_json_request(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate the body of an incoming JSON request.

    Parameters
    ----------
    req : dict
        A dictionary representing the HTTP request. It must contain at least:
            - "headers": a mapping of header names to values.
            - "body": the raw request body as bytes or str.

    Returns
    -------
    dict
        The parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type header is not application/json.
        If the body cannot be decoded as valid JSON.
    """
    # Ensure required keys exist
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary.")
    headers = req.get("headers")
    body = req.get("body")

    if headers is None or not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' in request.")
    if body is None:
        raise ValueError("Missing 'body' in request.")

    # Normalise header names to lower case for comparison
    content_type = headers.get("Content-Type") or headers.get("content-type")
    if not content_type:
        raise ValueError("Missing Content-Type header.")
    # Accept only application/json (optionally with charset)
    if not content_type.lower().startswith("application/json"):
        raise ValueError(
            f"Unsupported Content-Type: {content_type}. Expected application/json."
        )

    # Convert body to string if bytes
    if isinstance(body, bytes):
        try:
            body_text = body.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Unable to decode body bytes: {exc}") from exc
    elif isinstance(body, str):
        body_text = body
    else:
        raise ValueError("Body must be bytes or str.")

    # Parse JSON safely
    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object (dict).")

    # Optional CSRF protection: require X-CSRF-Token header if present
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token:
        # In a real application you would validate the token against session or cookie.
        # Here we simply check that it is a non‑empty string to demonstrate the check.
        if not isinstance(csrf_token, str) or not csrf_token.strip():
            raise ValueError("Invalid CSRF token.")

    return payload