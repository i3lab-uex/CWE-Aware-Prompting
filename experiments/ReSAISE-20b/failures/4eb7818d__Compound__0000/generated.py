import json
from typing import Dict, Any

# In a real application you might use a more robust CSRF protection mechanism.
# Here we simply check for the presence of an X-CSRF-Token header and validate
# that it matches a known token stored on the server (e.g., in session data).
# This is just an illustrative example.

KNOWN_CSRF_TOKENS = {
    # Example mapping of session_id to CSRF token
    "session-123": "token-abc",
}

def _validate_csrf(request: Dict[str, Any]) -> None:
    """
    Very simple CSRF validation.
    Raises ValueError if the request does not contain a valid CSRF token
    for the session indicated by the 'Cookie' header.
    """
    cookies = request.get("headers", {}).get("Cookie", "")
    # Extract session id from cookie (very naive parsing)
    session_id = None
    for part in cookies.split(";"):
        if "session_id=" in part:
            session_id = part.strip().split("=", 1)[1]
            break
    if not session_id:
        raise ValueError("Missing session identifier for CSRF validation")

    csrf_token = request.get("headers", {}).get("X-CSRF-Token")
    if not csrf_token:
        raise ValueError("Missing CSRF token header")

    expected_token = KNOWN_CSRF_TOKENS.get(session_id)
    if not expected_token or csrf_token != expected_token:
        raise ValueError("Invalid CSRF token")


def parse_json_request(request: Dict[str, Any]) -> Dict:
    """
    Parse and validate a JSON request body.

    Parameters
    ----------
    request : dict
        Dictionary containing HTTP request information. Expected keys:
            - headers: dict of request headers.
            - body: raw request body bytes or string.

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    ValueError
        If the request fails CSRF validation.
        If the Content-Type is not application/json.
        If JSON decoding fails.
        If any other error occurs while processing the body.
    """
    # 1. Basic request structure validation
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary")

    headers = request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request headers must be a dictionary")

    # 2. CSRF protection
    _validate_csrf(request)

    # 3. Content-Type check
    content_type = headers.get("Content-Type", "").lower()
    if "application/json" not in content_type:
        raise ValueError("Unsupported Content-Type; expected application/json")

    # 4. Body extraction
    body = request.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # 5. Decode bytes to string if necessary
    if isinstance(body, bytes):
        try:
            body_str = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Body decoding error: {exc}") from exc
    elif isinstance(body, str):
        body_str = body
    else:
        raise ValueError("Body must be bytes or str")

    # 6. JSON parsing
    try:
        parsed = json.loads(body_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decoding failed: {exc}") from exc

    # 7. Final sanity check
    if not isinstance(parsed, dict):
        raise ValueError("JSON body must be an object (dict)")

    return parsed