import re
from typing import Dict

# Mock database and CSRF token for demonstration purposes.
database: Dict[int, Dict[str, str]] = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@domain.org"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Simple regex for email validation (not exhaustive but sufficient for demo).
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")


def change_user_email(request_data: Dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and validating input.

    Args:
        request_data (dict): Represents the HTTP request. Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body": {
                    "user_id": <int>,
                    "new_email": "<string>"
                }
            }

    Returns:
        bool: True if the email was successfully updated, False otherwise.
    """
    # 1. CSRF token validation
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data safely
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate user_id
    if not isinstance(user_id, int):
        return False

    # 4. Validate new_email
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update email
    user_record["email"] = new_email
    return True

# Example usage:
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": "secure_csrf_token_123"},
        "body": {"user_id": 1, "new_email": "newemail@example.com"}
    }
    print(change_user_email(request))  # Should output: True