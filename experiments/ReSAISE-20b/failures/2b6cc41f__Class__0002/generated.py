import re

# Mock database and CSRF token for demonstration purposes.
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple email validation.
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def modify_user_email(req_data: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_data : dict
        A dictionary representing an HTTP request. It must contain:
            - headers: dict, with the key 'X-CSRF-Token' for CSRF protection.
            - body: dict, with keys 'user_id' (int) and 'new_email' (str).

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.

    Notes
    -----
    - CSRF token is verified against EXPECTED_CSRF_TOKEN.
    - The email address is validated with a simple regex.
    - Only existing user IDs are updated; otherwise, the function returns False.
    """
    # 1. Verify CSRF token
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch – reject the request
        return False

    # 2. Extract body parameters
    body = req_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate presence and types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check that the user exists
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # Any unexpected error results in a failure response
        return False


# Example usage (for testing purposes)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    success = modify_user_email(request)
    print("Update successful:", success)
    print("Updated database entry:", database[1])