import re

# Simulated database and CSRF token
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Simple email validation regex (RFC 5322 simplified)
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r"@([A-Za-z0-9](-?[A-Za-z0-9])*\.)+[A-Za-z]{2,}$)"
)

def change_user_email(query: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    query : dict
        The request containing:
            - headers: dict, must contain 'X-CSRF-Token'
            - body: dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Verify CSRF token
    headers = query.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = query.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate inputs
    if not isinstance(user_id, int) or user_id <= 0:
        return False

    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check user existence
    if user_id not in database:
        return False

    # 5. Update email
    try:
        database[user_id]["email"] = new_email.strip()
    except Exception:
        return False

    return True