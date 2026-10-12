import re
import hmac

# Mock database: {user_id: {"email": str, ...}}
database = {}

# Expected CSRF token for the session
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Simple regex for basic email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def modify_user_email(req_data: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Args:
        req_data (dict): HTTP request representation containing 'headers' and 'body'.

    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token using constant-time comparison
    try:
        csrf_token = req_data["headers"].get("X-CSRF-Token", "")
    except AttributeError:
        return False

    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract user ID and new email from the body
    try:
        body = req_data["body"]
        user_id = body.get("user_id")
        new_email = body.get("new_email")
    except AttributeError:
        return False

    if not user_id or not new_email:
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Prevent trivial injection by ensuring new_email is a string
    if not isinstance(new_email, str):
        return False

    # 5. Perform the update
    user_record["email"] = new_email.strip()
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Setup a sample user
    database["user123"] = {"email": "old@example.com"}

    # Construct a request
    request = {
        "headers": {"X-CSRF-Token": "secure_csrf_token_12345"},
        "body": {"user_id": "user123", "new_email": "new@example.com"}
    }

    print(modify_user_email(request))  # Should output: True
    print(database["user123"]["email"])  # Should output: new@example.com