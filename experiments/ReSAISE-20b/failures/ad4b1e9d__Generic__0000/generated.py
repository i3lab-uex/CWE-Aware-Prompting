import typing as _t

# Simulated data store and CSRF token (these would normally be global or injected)
database: _t.Dict[int, _t.Any] = {}
EXPECTED_CSRF_TOKEN: str = "expected_token_value"

def erase_user_profile(req_payload: _t.Dict[str, _t.Any]) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    req_payload : dict
        HTTP request representation. Expected keys:
            - 'headers': a mapping containing the CSRF token under
              'X-CSRF-Token' (case‑insensitive).
            - 'body': a mapping containing the user identifier under
              'user_id'.

    Returns
    -------
    bool
        ``True`` if the user was successfully deleted,
        ``False`` otherwise (missing data, CSRF mismatch or
        non‑existent user).
    """
    # Basic validation of the request structure
    if not isinstance(req_payload, dict):
        return False

    headers = req_payload.get("headers")
    body   = req_payload.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # Extract CSRF token (case‑insensitive key lookup)
    csrf_token = None
    for key, value in headers.items():
        if isinstance(key, str) and key.lower() == "x-csrf-token":
            csrf_token = value
            break

    if not isinstance(csrf_token, str) or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # Perform deletion atomically
    try:
        # Using pop to avoid KeyError and return None if missing
        removed = database.pop(user_id, None)
    except Exception:
        # Any unexpected error during deletion results in False
        return False

    return removed is not None