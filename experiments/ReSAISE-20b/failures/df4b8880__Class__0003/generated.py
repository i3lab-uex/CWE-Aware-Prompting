import re
from hmac import compare_digest

# Simulated database: {user_id: {"email": "old@example.com"}}
database = {}

# Predefined CSRF token (for demonstration purposes)
EXPECTED_CSRF_TOKEN = "s3cureT0k3n123"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def alter_user_email(payload: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    payload : dict
        Request data containing:
            - headers: dict, may include 'X-CSRF-Token'
            - body: dict, must contain 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF token validation (constant‑time comparison)
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract body data
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate presence of required fields
    if user_id is None or new_email is None:
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Verify user exists
    if user_id not in database:
        return False

    # 6. Update email
    database[user_id]["email"] = new_email
    return True

# Example usage (for testing only; remove in production)
if __name__ == "__main__":
    # Seed the mock database
    database["user123"] = {"email": "old@example.com"}

    # Valid request
    payload_valid = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "new_email": "new@example.com"}
    }
    assert alter_user_email(payload_valid) is True
    assert database["user123"]["email"] == "new@example.com"

    # Invalid CSRF token
    payload_bad_csrf = {
        "headers": {"X-CSRF-Token": "badtoken"},
        "body": {"user_id": "user123", "new_email": "another@example.com"}
    }
    assert alter_user_email(payload_bad_csrf) is False

    # Invalid email format
    payload_bad_email = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "new_email": "not-an-email"}
    }
    assert alter_user_email(payload_bad_email) is False