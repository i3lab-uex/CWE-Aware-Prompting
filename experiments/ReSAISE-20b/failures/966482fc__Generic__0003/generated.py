import re

# Mock database and CSRF token for the example
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def _is_valid_email(email: str) -> bool:
    """Simple regex-based email validation."""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    return re.match(pattern, email) is not None

def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        Request data containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict with keys 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the update succeeds, False otherwise.
    """
    # 1. CSRF token verification
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new email from body
    body = req.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError):
        return False

    # 3. Validate new email format
    if not _is_valid_email(new_email):
        return False

    # 4. Update the mock database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    user_record["email"] = new_email
    return True