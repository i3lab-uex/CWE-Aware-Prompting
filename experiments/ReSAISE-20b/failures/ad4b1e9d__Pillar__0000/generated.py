import json

# Simulated in‑memory database of users (user_id -> user_info)
database: dict[str, dict] = {
    "alice": {"name": "Alice", "email": "alice@example.com"},
    "bob":   {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token for the current session
EXPECTED_CSRF_TOKEN: str = "securetoken123"


def erase_user_profile(req_payload: dict) -> bool:
    """
    Deletes a user account from the in‑memory database.

    Parameters
    ----------
    req_payload : dict
        A dictionary containing request data. Expected keys:
            - "headers": dict, may contain a "X-CSRF-Token" header.
            - "body": str or dict, JSON‑encoded body containing a "user_id" field.

    Returns
    -------
    bool
        True if the user was found and deleted, False otherwise.

    Notes
    -----
    - The function validates the CSRF token to mitigate CWE‑693 (Protection Mechanism Failure).
    - It checks that the user ID is a non‑empty string before attempting deletion.
    - All failures return False without raising exceptions to avoid leaking internal state.
    """
    try:
        # 1. CSRF token validation
        headers = req_payload.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            # Token missing or incorrect
            return False

        # 2. Parse request body
        body = req_payload.get("body")
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                return False
        if not isinstance(body, dict):
            return False

        # 3. Extract user ID
        user_id = body.get("user_id")
        if not isinstance(user_id, str) or not user_id:
            return False

        # 4. Delete the user if it exists
        if user_id in database:
            del database[user_id]
            return True

        # User not found
        return False

    except Exception:
        # Any unexpected error should not expose details
        return False