import re
from typing import Dict, Any

# Mock database and CSRF token used in the application
database: Dict[int, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def edit_user_email(req_payload: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_payload : dict
        Dictionary containing request headers and body. Expected keys:
            - 'headers': mapping of HTTP header names to values
            - 'body': mapping containing:
                * 'user_id' (int): Identifier of the user to update
                * 'new_email' (str): The new email address

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    - Validates CSRF token from the 'X-CSRF-Token' header.
    - Performs basic email format validation.
    - Returns False if the user does not exist, token is missing/incorrect,
      or email format is invalid.
    """
    # 1. Validate CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = req_payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Update database
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # Update the email
    user_record["email"] = new_email
    return True


# ------------------------------------------------------------------
# Example usage (for illustration only; remove in production)
if __name__ == "__main__":
    # Seed mock database
    database[1] = {"email": "old@example.com", "name": "Alice"}

    # Create a request payload
    payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }

    success = edit_user_email(payload)
    print("Update successful:", success)          # Expected: True
    print("New email:", database[1]["email"])     # Expected: alice.new@example.com