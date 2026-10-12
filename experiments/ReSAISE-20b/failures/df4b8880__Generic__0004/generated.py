import re
from typing import Dict

# Global mock database and CSRF token
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

# Simple regex for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def alter_user_email(payload: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Args:
        payload: dict containing request headers and body data.
            Expected structure:
                {
                    "headers": {"CSRF-Token": "..."},
                    "body": {"user_id": int, "email": str}
                }

    Returns:
        True if the email was successfully updated, False otherwise.
    """
    # Validate payload structure
    headers = payload.get("headers", {})
    body = payload.get("body", {})

    # CSRF protection
    csrf_token = headers.get("CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID and new email
    try:
        user_id = int(body["user_id"])
        new_email = str(body["email"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # Basic email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # Check that user exists in the database
    if user_id not in database:
        return False

    # Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        return False

    return True


# Example usage (for testing purposes only):
if __name__ == "__main__":
    # Setup a mock user
    database[1] = {"email": "old@example.com", "name": "Alice"}

    # Successful update
    payload_success = {
        "headers": {"CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "email": "newalice@example.com"},
    }
    print(alter_user_email(payload_success))  # True

    # Failed update (wrong CSRF)
    payload_fail_csrf = {
        "headers": {"CSRF-Token": "wrong_token"},
        "body": {"user_id": 1, "email": "bad@example.com"},
    }
    print(alter_user_email(payload_fail_csrf))  # False