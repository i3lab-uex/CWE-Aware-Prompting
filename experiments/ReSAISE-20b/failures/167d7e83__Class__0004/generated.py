import re

# Simulated database of users: {user_id: {"email": str, ...}}
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token for the request
EXPECTED_CSRF_TOKEN = "expected_csrf_token_value"

# Regular expression for a very basic email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")

def update_user_email(request: dict) -> bool:
    """
    Update a user's email address after validating the request.

    Args:
        request: dict containing at least the following keys:
            - "headers": dict of HTTP headers (must include "X-CSRF-Token")
            - "body": dict with keys "user_id" (int) and "new_email" (str)

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate user_id
    body = request.get("body", {})
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False
    user = database.get(user_id)
    if not user:
        return False

    # 3. Validate new email format
    new_email = body.get("new_email")
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the email
    user["email"] = new_email
    return True

# Example usage:
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(update_user_email(req))          # True
    print(database[1]["email"])            # alice.new@example.com