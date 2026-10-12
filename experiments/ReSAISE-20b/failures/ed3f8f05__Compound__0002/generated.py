import re
from typing import Dict, Any

# Mock database and CSRF token for demonstration purposes.
database: Dict[int, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def _is_valid_email(email: str) -> bool:
    """Return True if the email matches a basic pattern."""
    return isinstance(email, str) and EMAIL_REGEX.match(email) is not None

def change_user_email(request_data: Dict[str, Any]) -> bool:
    """
    Update a user's email address after verifying CSRF token and input validity.

    Parameters
    ----------
    request_data : dict
        Dictionary containing at least the keys 'headers' and 'body'.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id": <int>,
                    "new_email": "<email>"
                }
            }

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. CSRF protection
    headers = request_data.get("headers", {})
    token = headers.get("X-CSRF-Token")
    if token != EXPECTED_CSRF_TOKEN:
        # Token missing or invalid
        return False

    # 2. Retrieve and validate body data
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # Basic type checks
    if not isinstance(user_id, int):
        return False
    if not _is_valid_email(new_email):
        return False

    # 3. Update the mock database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Update the email
    user_record["email"] = new_email.strip()
    return True

# Example usage (for testing only)
if __name__ == "__main__":
    # Setup mock data
    database[42] = {"email": "old@example.com", "name": "Alice"}

    # Correct request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 42, "new_email": "alice@example.com"}
    }
    print(change_user_email(req))  # Expected: True
    print(database[42]["email"])   # Expected: alice@example.com

    # Wrong CSRF token
    req_bad_token = {
        "headers": {"X-CSRF-Token": "badtoken"},
        "body": {"user_id": 42, "new_email": "alice@example.com"}
    }
    print(change_user_email(req_bad_token))  # Expected: False