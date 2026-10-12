import re
import hmac
from typing import Dict, Any

# Mock database and CSRF token (for demonstration purposes)
database: Dict[int, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "s3cUrE12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def _is_valid_email(email: str) -> bool:
    """Return True if the email matches a simple RFC‑5322 pattern."""
    return bool(EMAIL_REGEX.match(email))


def change_user_email(request_data: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    request_data : dict
        HTTP request representation. Must contain:
            - 'headers': dict with at least a 'X-CSRF-Token' entry.
            - 'body': dict containing 'user_id' (int) and 'new_email' (str).

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.

    Notes
    -----
    - Uses constant‑time comparison for the CSRF token to mitigate timing attacks.
    - Validates that the new email address has a reasonable format before updating.
    - Checks that the user exists in the database; if not, returns False.
    """
    # 1. Verify CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        # Invalid or missing CSRF token
        return False

    # 2. Extract user data from body
    body = request_data.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, TypeError, ValueError):
        # Missing or malformed data
        return False

    # 3. Validate email format
    if not isinstance(new_email, str) or not _is_valid_email(new_email):
        return False

    # 4. Update the mock database
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    user_record["email"] = new_email
    # In a real application, you would persist the change to storage here.

    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate mock database
    database[42] = {"email": "old@example.com", "name": "Alice"}

    # Construct a request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 42, "new_email": "alice@example.com"},
    }

    print(change_user_email(req))  # Expected: True
    print(database[42]["email"])   # Expected: "alice@example.com"