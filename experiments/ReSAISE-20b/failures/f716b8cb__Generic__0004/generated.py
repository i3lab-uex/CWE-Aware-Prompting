import re
from typing import Dict

# Simulated database and CSRF token (would normally be external)
database: Dict[int, Dict[str, str]] = {
    1: {"email": "old@example.com", "name": "Alice"},
    2: {"email": "bob@sample.org", "name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Simple email validation regex
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}"
    r"[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$"
)


def modify_user_email_address(user_request: Dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    user_request : dict
        Incoming request containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body fields
    body = user_request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Ensure user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update email
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # Log exception in real application; here we simply fail gracefully
        return False


# Example usage (would be removed or replaced by unit tests)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(modify_user_email_address(request))  # Expected: True
    print(database[1]["email"])                # Updated email