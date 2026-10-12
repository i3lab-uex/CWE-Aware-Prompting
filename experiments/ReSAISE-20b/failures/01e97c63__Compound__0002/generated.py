import json
from typing import Dict

class CSRFError(ValueError):
    """Raised when a required CSRF token is missing or invalid."""
    pass

def handle_json_input(client_request: Dict) -> Dict:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    client_request : dict
        Dictionary containing the HTTP request headers and body.
        Expected keys are:
            - "headers": dict of request headers
            - "body": raw request body as bytes or str

    Returns
    -------
    dict
        Parsed JSON payload.

    Raises
    ------
    ValueError
        If the Content-Type is not a JSON-compatible type.
    ValueError
        If the body contains malformed JSON.
    CSRFError
        If a required CSRF token header is missing or empty.

    Notes
    -----
    * The function checks for common JSON MIME types.
    * For CSRF protection it expects a non-empty `X-CSRF-Token` header
      (or an equivalent token).  In production, you would validate the
      token against a session store or JWT.
    """
    headers = client_request.get("headers", {})
    body = client_request.get("body")

    # ------------------------------------------------------------------
    # 1. Validate Content-Type
    # ------------------------------------------------------------------
    content_type = headers.get("Content-Type", "")
    if not isinstance(content_type, str):
        raise ValueError("Content-Type header must be a string")

    # Accept common JSON MIME types
    json_mime_types = {
        "application/json",
        "application/json; charset=utf-8",
        "application/json;charset=UTF-8",
    }
    # Normalize: lower case, strip whitespace
    normalized_ct = content_type.strip().lower()
    if not any(normalized_ct.startswith(mime) for mime in json_mime_types):
        raise ValueError(
            f"Unsupported Content-Type: '{content_type}'. "
            "Expected 'application/json'."
        )

    # ------------------------------------------------------------------
    # 2. CSRF protection
    # ------------------------------------------------------------------
    csrf_token = headers.get("X-CSRF-Token") or headers.get("X-XSRF-TOKEN")
    if not csrf_token:
        raise CSRFError(
            "Missing required CSRF token header (X-CSRF-Token or X-XSRF-TOKEN)."
        )
    if not isinstance(csrf_token, str) or csrf_token.strip() == "":
        raise CSRFError("CSRF token must be a non-empty string.")

    # ------------------------------------------------------------------
    # 3. Parse JSON body
    # ------------------------------------------------------------------
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Request body is not valid UTF-8.") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Request body must be a string or bytes.")

    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Malformed JSON in request body.") from exc

    if not isinstance(parsed, dict):
        raise ValueError("JSON payload must be an object (dict).")

    return parsed