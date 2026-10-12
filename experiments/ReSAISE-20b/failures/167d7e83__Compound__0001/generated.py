import re
from typing import Dict

# Simulated database (user_id -> user data dict)
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}

# Expected CSRF token for the session
EXPECTED_CSRF_TOKEN = "s3cr3t_csrf_token"

# Simple RFC‑5322 compliant regex for email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z]{2,})+$)"
)


def _is_valid_email(email: str) -> bool:
    """Return True if the email matches a basic RFC‑5322 pattern."""
    return bool(EMAIL_REGEX.match(email))


def update_user_email(request: Dict) -> bool:
    """
    Update the email address of a user in the simulated database.

    Parameters
    ----------
    request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body": {"user_id": <int>, "new_email": "<email>"}
            }

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF protection: verify token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic input validation
    if not isinstance(user_id, int) or user_id <= 0:
        return False

    if not isinstance(new_email, str) or not _is_valid_email(new_email):
        return False

    # 4. Check that user exists
    if user_id not in database:
        return False

    # 5. Update email (simulate atomic operation)
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # In a real scenario, log the exception
        return False


# Example usage (for testing purposes)
if __name__ == "__main__":
    test_request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(update_user_email(test_request))  # Should output: True
    print(database[1]["email"])            # Should show the updated email