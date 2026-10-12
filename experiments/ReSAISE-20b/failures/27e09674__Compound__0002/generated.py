import re

# Simulated database of users: {user_id: {"email": ...}}
database = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.org"},
}

# Expected CSRF token that must be present in the request headers
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$")


def change_user_email(query: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and email format.

    Parameters
    ----------
    query : dict
        Request dictionary containing:
            - 'headers': dict of HTTP headers, must include 'X-CSRF-Token'
            - 'body': dict with keys 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate presence of required keys
    if not isinstance(query, dict):
        return False

    headers = query.get("headers", {})
    body = query.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Reject requests without the correct CSRF token
        return False

    # 3. Extract user ID and new email
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 4. Basic email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check that the user exists in the database
    if user_id not in database:
        return False

    # 6. Update the user's email
    database[user_id]["email"] = new_email

    return True