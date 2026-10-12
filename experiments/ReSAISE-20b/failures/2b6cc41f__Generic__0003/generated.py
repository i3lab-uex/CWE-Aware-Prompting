import re

# Mock database and CSRF token for the example
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"}
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

def modify_user_email(req_data: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": dict containing a "X-CSRF-Token" entry.
            - "body": dict containing:
                * "user_id": int
                * "new_email": str

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. CSRF protection
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new email
    body = req_data.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Basic email validation
    if not isinstance(new_email, str):
        return False
    email_regex = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )
    if not email_regex.match(new_email):
        return False

    # 4. Update the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Prevent accidental overwrite with same value
    if user_record.get("email") == new_email:
        return True

    # 5. Perform the update
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # In a real scenario, log the exception
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": "secure-token-123"},
        "body": {"user_id": 1, "new_email": "alice@newdomain.com"}
    }
    print(modify_user_email(request))  # Expected: True