import re

# Simulated database and CSRF token (these would normally be provided by the framework)
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Simple email validation regex (not exhaustive but sufficient for most cases)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$)"
)


def update_user_email(request: dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    request : dict
        Expected to contain:
            - headers: dict with 'X-CSRF-Token'
            - body:   dict with keys:
                * 'user_id' (int)
                * 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic validation of input types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check that the user exists in the database
    if user_id not in database:
        return False

    # 6. Update the email address
    database[user_id]["email"] = new_email.strip()

    return True