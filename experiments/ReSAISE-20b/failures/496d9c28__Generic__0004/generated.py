import re

# Simulated database (user_id -> user record)
database = {
    1: {"email": "alice@example.com", "name": "Alice"},
    2: {"email": "bob@example.com", "name": "Bob"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure_token_123"

def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    new_request : dict
        The incoming request object containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict with keys 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body fields
    body = new_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"].strip()
    except (KeyError, ValueError):
        return False

    # 3. Validate email format
    if not re.fullmatch(
        r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
        r"@([A-Za-z0-9]([-A-Za-z0-9]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}$)",
        new_email,
    ):
        return False

    # 4. Ensure user exists
    if user_id not in database:
        return False

    # 5. Update the email
    database[user_id]["email"] = new_email
    return True

# Example usage (for testing only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(change_user_email(request))  # Should output: True
    print(database[1]["email"])        # Should show updated email