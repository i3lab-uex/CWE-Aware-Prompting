import re
import hmac
from typing import Dict

# Mock database and CSRF token for demonstration purposes.
database: Dict[str, dict] = {
    "1": {"email": "old@example.com"},
    "2": {"email": "user2@example.org"}
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_value"

# Regular expression for basic email validation.
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def alter_user_email(payload: Dict) -> bool:
    """
    Update a user's email address after verifying CSRF protection
    and validating input data.

    Args:
        payload: dict containing at least the following keys:
            - 'headers': dict with a 'X-CSRF-Token' entry
            - 'body': dict with 'user_id' and 'new_email'

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. Extract and validate CSRF token using constant‑time comparison
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract body data
    body = payload.get("body", {})
    user_id = str(body.get("user_id"))  # Ensure string key
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the mock database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["email"] = new_email
    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    test_payload = {
        "headers": {"X-CSRF-Token": "secure_csrf_token_value"},
        "body": {"user_id": 1, "new_email": "new.email@example.com"}
    }
    print(alter_user_email(test_payload))  # Should output: True