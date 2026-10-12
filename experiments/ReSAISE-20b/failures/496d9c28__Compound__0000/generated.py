import json
import re

# Simulated database: mapping user_id (int) -> dict with 'email' field
database = {
    1: {'email': 'alice@example.com'},
    2: {'email': 'bob@example.com'},
}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$)"
)

def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and input validity.

    Args:
        new_request (dict): Request object containing 'headers' and 'body'.
            Expected keys:
                - headers['X-CSRF-Token']: str
                - body: JSON string with keys 'user_id' (int) and 'new_email' (str)

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Parse request body (JSON)
    try:
        body_str = new_request.get("body", "")
        data = json.loads(body_str)
    except (json.JSONDecodeError, TypeError):
        return False

    # 3. Validate required fields
    user_id = data.get("user_id")
    new_email = data.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check that user exists in the database
    if user_id not in database:
        return False

    # 6. Update the email
    database[user_id]["email"] = new_email
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": 1, "new_email": "alice.new@example.org"})
    }
    result = change_user_email(request)
    print("Update successful:", result)
    print("Updated database entry:", database[1])