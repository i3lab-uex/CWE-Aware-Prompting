import re
import hmac
from typing import Dict, Any

# Pre‑defined CSRF token for the application (should be stored securely)
EXPECTED_CSRF_TOKEN = "s3cr3t-t0k3n"

# Mock database: key is user id, value is a dict with user data
database: Dict[str, Dict[str, Any]] = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.org"},
}

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    return hmac.compare_digest(val1, val2)


def _is_valid_email(email: str) -> bool:
    """
    Basic validation of email format.
    """
    return bool(EMAIL_REGEX.match(email))


def alter_user_email(payload: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    payload : dict
        Expected keys:
            - 'headers': dict containing the CSRF token under key 'X-CSRF-Token'
            - 'body'   : dict containing:
                * 'user_id': str
                * 'new_email': str

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    - The function performs constant‑time CSRF token comparison to avoid timing attacks.
    - Email format is validated before updating the database.
    - The function checks that the user exists in the mock database.
    """
    # 1. Validate payload structure
    if not isinstance(payload, dict):
        return False

    headers = payload.get("headers", {})
    body = payload.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False
    if not _constant_time_compare(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Extract user id and new email
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, str) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 5. Check user exists in the database
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # 6. Perform the update
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # In a real application, log the exception here
        return False


# Example usage (for manual testing)
if __name__ == "__main__":
    test_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "1", "new_email": "alice.new@example.com"},
    }
    print(alter_user_email(test_payload))  # Should output: True
    print(database["1"]["email"])          # Should show updated email