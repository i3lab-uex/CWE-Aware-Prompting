import re
from typing import Dict

# Mock database: user_id -> dict with 'email' field
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token (in a real app this would be stored per session)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Simple email regex for validation (not fully RFC compliant, but sufficient for demo)
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]{2,}$")


def edit_user_email(req_payload: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_payload : dict
        A dictionary representing an HTTP request. Expected keys:
            - "headers": a dict containing request headers.
            - "body": a dict containing user data:
                * "user_id" (int): the ID of the user to update.
                * "new_email" (str): the new email address.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """

    # 1. CSRF protection: ensure request contains the expected token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or invalid – reject the request
        return False

    # 2. Extract body data
    body = req_payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic validation of input
    if not isinstance(user_id, int) or user_id <= 0:
        return False

    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    try:
        user_record["email"] = new_email.strip()
    except Exception:
        # Unexpected error during update
        return False

    return True


# Example usage (for testing only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(edit_user_email(request))  # Expected: True
    print(database[1]["email"])      # Expected: alice.new@example.com