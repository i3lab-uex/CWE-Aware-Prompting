import re
from typing import Dict

# Constants used by the function
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def alter_user_email(payload: Dict[str, any], database: Dict[int, dict]) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    payload : dict
        Dictionary representing the request. Expected keys:
            - "headers": dict containing a "X-CSRF-Token" key.
            - "body": dict containing:
                - "user_id": int
                - "new_email": str
    database : dict
        Mock database mapping user IDs to user data dictionaries.
        The user's "email" field will be updated if validation passes.

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or incorrect
        return False

    # 2. Extract body data
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate presence and types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Ensure user exists
    if user_id not in database:
        return False

    # 6. Update the email
    try:
        database[user_id]["email"] = new_email.strip()
    except Exception:
        # In case the user record is not a dict or other unexpected issue
        return False

    return True


# Example usage (for testing purposes only; remove in production)
if __name__ == "__main__":
    # Mock database
    db = {
        1: {"email": "old@example.com", "name": "Alice"},
        2: {"email": "bob@sample.org", "name": "Bob"},
    }

    # Sample payload
    request_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }

    result = alter_user_email(request_payload, db)
    print("Update successful:", result)
    print("Updated database entry:", db[1])