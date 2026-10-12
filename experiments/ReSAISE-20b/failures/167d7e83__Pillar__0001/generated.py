import re

# Simulated database: user_id -> { "email": str, ... }
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "secure-token-123"

EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z]{2,})+$)"
)


def update_user_email(request: dict) -> bool:
    """
    Update a user's email address.

    Parameters
    ----------
    request : dict
        Expected keys:
            - headers: dict containing 'X-CSRF-Token'
            - body: dict containing 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """

    # 1. CSRF token validation
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate request body
    body = request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"].strip()
    except (KeyError, ValueError, AttributeError):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check user existence
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update
    try:
        user_record["email"] = new_email
    except Exception:
        # Any unexpected error during update should not expose internals
        return False

    return True