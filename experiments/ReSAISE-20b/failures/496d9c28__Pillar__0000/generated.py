import re

# Simulated database: {user_id: {"email": str, ...}}
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")


def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Args:
        new_request (dict): Incoming request containing headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body":   {
                        "user_id": <int>,
                        "new_email": "<string>"
                    }
                }

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract user ID and new email from body
    body = new_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError):
        # Missing or invalid fields
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that the user exists in the database
    if user_id not in database:
        return False

    # 5. Update the email
    database[user_id]["email"] = new_email
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"}
    }
    print("Update successful:", change_user_email(request))
    print("Updated user record:", database[1])