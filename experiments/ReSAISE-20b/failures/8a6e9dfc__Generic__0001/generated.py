import re
from typing import Dict, Any

# Simulated environment variables / constants
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def is_valid_email(email: str) -> bool:
    """Return True if the email matches a simple RFC 5322 pattern."""
    return isinstance(email, str) and bool(EMAIL_REGEX.match(email))


def edit_user_email(payload: Dict[str, Any], database: Dict[int, Dict[str, Any]]) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    payload : dict
        Incoming request containing 'headers' and 'body'.
        Example:
            {
                "headers": {"X-CSRF-Token": "..."},
                "body":   {"user_id": 42, "new_email": "foo@example.com"}
            }
    database : dict
        Simulated database mapping user IDs to a dict of attributes.
        Example:
            {42: {"email": "old@example.com", ...}, ...}

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Notes
    -----
    - Validates CSRF token.
    - Checks that the user exists in the database.
    - Validates the new email format.
    """
    # 1. CSRF token validation
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic sanity checks
    if not isinstance(user_id, int) or user_id <= 0:
        return False

    if not is_valid_email(new_email):
        return False

    # 4. Check that the user exists
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # 5. Update email
    user_record["email"] = new_email
    return True

# Example usage (for testing purposes)
if __name__ == "__main__":
    db = {1: {"email": "old@example.com"}}
    req_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "new@example.com"},
    }
    print(edit_user_email(req_payload, db))  # Should output: True
    print(db[1]["email"])                   # Should output: new@example.com