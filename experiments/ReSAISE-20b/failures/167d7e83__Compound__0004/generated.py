import re

# Simulated database and CSRF token (would normally be stored securely)
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"}
}
EXPECTED_CSRF_TOKEN = "secure_token_12345"

# Simple email regex pattern (not exhaustive but sufficient for demo)
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")

def update_user_email(request: dict) -> bool:
    """
    Update the email address of a user.

    Parameters
    ----------
    request : dict
        Dictionary containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Potential CSRF attack or missing token
        return False

    # 2. Extract and validate payload
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or user_id not in database:
        # Invalid or non-existent user
        return False

    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        # Invalid email format
        return False

    # 3. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Catch unexpected errors (e.g., database write failure)
        return False

    return True