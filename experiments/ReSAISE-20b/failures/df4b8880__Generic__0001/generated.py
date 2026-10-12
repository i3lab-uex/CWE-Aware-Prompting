import re
from typing import Dict, Any

# Predefined CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Simple email regex pattern (RFC 5322 compliant is complex; this covers most common cases)
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")


def alter_user_email(payload: Dict[str, Any], database: Dict[int, Dict[str, Any]]) -> bool:
    """
    Update a user's email address in the mock database.

    Args:
        payload: Dictionary containing request data.
                 Expected structure:
                     {
                         "headers": {"X-CSRF-Token": "..."},
                         "body":   {"user_id": 1, "new_email": "example@domain.com"}
                     }
        database: Dictionary simulating the user data store.
                  Keys are integer user IDs, values are dicts with at least an "email" key.

    Returns:
        True if the email was successfully updated, False otherwise.
    """
    try:
        # Extract headers and body
        headers = payload.get("headers", {})
        body = payload.get("body", {})

        # CSRF token validation
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # Extract user ID and new email
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        # Basic validation
        if not isinstance(user_id, int) or user_id <= 0:
            return False

        if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
            return False

        # Check user existence
        if user_id not in database:
            return False

        # Update email
        database[user_id]["email"] = new_email.strip()
        return True

    except Exception:
        # In production, log the exception details
        return False


# Example usage (for demonstration purposes only; remove in production)
if __name__ == "__main__":
    # Mock database
    db = {
        1: {"email": "old@example.com"},
        2: {"email": "user2@domain.org"}
    }

    # Valid payload
    request_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "newemail@example.com"}
    }

    success = alter_user_email(request_payload, db)
    print(f"Update successful: {success}")
    print(f"Updated database: {db}")