import json

# Simulated database and CSRF token for demonstration purposes.
database = {
    "1": {"name": "Alice", "email": "alice@example.com"},
    "2": {"name": "Bob",   "email": "bob@example.com"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def erase_user_profile(req_payload: dict) -> bool:
    """
    Deletes a user profile from the simulated database.

    Parameters
    ----------
    req_payload : dict
        The HTTP request payload. Expected to contain:
            - headers: dict with 'X-CSRF-Token' key.
            - body: JSON string or dict containing a 'user_id' field.

    Returns
    -------
    bool
        True if the user was deleted successfully, False otherwise.
    """
    try:
        # 1. CSRF protection
        headers = req_payload.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False  # CSRF validation failed

        # 2. Parse body and extract user_id
        body = req_payload.get("body")
        if isinstance(body, str):
            try:
                body_data = json.loads(body)
            except json.JSONDecodeError:
                return False
        elif isinstance(body, dict):
            body_data = body
        else:
            return False

        user_id = str(body_data.get("user_id"))
        if not user_id:
            return False  # No user ID provided

        # 3. Delete the user if it exists
        if user_id in database:
            del database[user_id]
            return True

        # User not found
        return False

    except Exception:
        # Log exception in real-world scenario; suppress here.
        return False