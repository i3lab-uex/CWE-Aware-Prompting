import re
import hmac

# Simulated database and CSRF token (for demonstration purposes)
database: dict = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

# Simple regex for basic email validation
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$")


def edit_user_email(payload: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Args:
        payload (dict): Incoming request containing headers and body.
            Expected format:
                {
                    "headers": {"X-CSRF-Token": "..."},
                    "body":   {"user_id": "...", "new_email": "..."}
                }

    Returns:
        bool: True if update succeeded, False otherwise.

    Raises:
        None
    """
    # 1. Validate CSRF token using constant‑time comparison to mitigate timing attacks.
    try:
        request_token = payload["headers"]["X-CSRF-Token"]
    except KeyError:
        return False

    if not hmac.compare_digest(request_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract user ID and new email from body.
    try:
        body = payload["body"]
        user_id = body["user_id"]
        new_email = body["new_email"].strip()
    except (KeyError, AttributeError):
        return False

    # 3. Basic email format validation.
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update the simulated database if user exists.
    if user_id not in database:
        return False

    # 5. Perform the update.
    try:
        database[user_id]["email"] = new_email
    except Exception:
        return False

    return True