import json

# Mock database and CSRF token for demonstration purposes
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def remove_user_account(req: dict) -> bool:
    """
    Remove a user account identified by `user_id` from the in-memory `database`.

    Parameters
    ----------
    req : dict
        Representation of an HTTP request containing:
            - headers: dict with 'X-CSRF-Token' key
            - body   : JSON string or dict containing 'user_id'

    Returns
    -------
    bool
        True if the account was successfully removed, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Validate CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract user_id from body
    raw_body = req.get("body")
    if raw_body is None:
        raise ValueError("Request body missing")

    # Body may be a JSON string or already parsed dict
    if isinstance(raw_body, str):
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise ValueError("Body is not valid JSON") from exc
    elif isinstance(raw_body, dict):
        body = raw_body
    else:
        raise ValueError("Unsupported body format")

    user_id = body.get("user_id")
    if user_id is None:
        raise ValueError("Missing 'user_id' in request body")

    # Ensure user_id is an integer (or convertible to int)
    try:
        user_id = int(user_id)
    except (TypeError, ValueError) as exc:
        raise ValueError("user_id must be an integer") from exc

    # 3. Perform deletion
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False