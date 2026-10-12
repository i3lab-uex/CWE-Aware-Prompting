import re
from typing import Dict

# Simulated database and CSRF token (these would normally be provided by the caller)
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

# Simple email validation regex
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def edit_user_email(payload: Dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    payload : dict
        Incoming request data. Expected keys:
            - 'headers': dict containing at least 'X-CSRF-Token'
            - 'body': dict containing 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # Validate presence of headers and body
    if not isinstance(payload, dict):
        return False

    headers = payload.get("headers", {})
    body = payload.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract and validate user ID
    try:
        user_id = int(body.get("user_id"))
    except (TypeError, ValueError):
        return False

    # Validate new email format
    new_email = body.get("new_email")
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # Check that the user exists in the database
    if user_id not in database:
        return False

    # Update the email address
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # In a real application, log the exception here
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate the simulated database
    database[1] = {"email": "old@example.com", "name": "Alice"}

    # Construct a payload
    test_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice@example.com"},
    }

    print(edit_user_email(test_payload))  # Should output: True
    print(database[1]["email"])          # Should output: alice@example.com