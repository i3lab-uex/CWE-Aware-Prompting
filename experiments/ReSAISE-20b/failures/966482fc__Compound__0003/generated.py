import re

# Mock database and CSRF token for demonstration purposes
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Simple email validation regex (RFC 5322 is complex; this covers common cases)
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address in the mock database after performing
    CSRF protection, input validation, and existence checks.

    Parameters:
        req (dict): Request data containing headers and body.
                    Expected structure:
                        {
                            "headers": {"X-CSRF-Token": "..."},
                            "body":   {"user_id": int, "new_email": str}
                        }

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF protection
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid
        return False

    # 2. Extract body data
    body = req.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate input types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check user existence
    if user_id not in database:
        return False

    # 6. Update email
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unforeseen error during update should not expose details
        return False

    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"}
    }
    print(modify_user_email(request))  # Should output: True
    print(database[1]["email"])        # Should show the updated email