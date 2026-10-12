import re
import hmac

# Constants and mock database (would normally be defined elsewhere)
EXPECTED_CSRF_TOKEN = "secure_token_12345"
database: dict[str, dict] = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@example.com"},
}

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def _is_valid_email(email: str) -> bool:
    """Check if the email matches a simple RFC‑5322 compliant pattern."""
    return bool(EMAIL_REGEX.match(email))

def alter_user_email(payload: dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and input validity.

    Args:
        payload: Dictionary containing 'headers' (dict) and 'body' (dict).
                 Expected keys in body: 'user_id' (int or str) and 'new_email' (str).

    Returns:
        True if the email was updated successfully, False otherwise.
    """
    # Basic payload structure checks
    try:
        headers = payload["headers"]
        body = payload["body"]
    except KeyError:
        return False

    # CSRF token verification (constant‑time comparison)
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract and validate user ID
    try:
        user_id = int(body["user_id"])
    except (KeyError, ValueError):
        return False

    # Validate new email format
    new_email = body.get("new_email", "")
    if not isinstance(new_email, str) or not _is_valid_email(new_email):
        return False

    # Ensure user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    try:
        user_record["email"] = new_email
    except Exception:
        # Any unexpected error during assignment should result in failure
        return False

    return True