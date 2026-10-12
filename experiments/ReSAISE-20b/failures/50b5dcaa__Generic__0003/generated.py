import re
from typing import Dict

# Constants for CSRF validation
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

# Mock database: mapping user_id (int) to a dict containing user data
database: Dict[int, Dict[str, str]] = {
    1: {"email": "old@example.com", "name": "Alice"},
    2: {"email": "bob@sample.org", "name": "Bob"},
}

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def _is_valid_email(email: str) -> bool:
    """Return True if the email matches a basic pattern."""
    return EMAIL_REGEX.match(email) is not None


def edit_user_email(req_payload: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_payload : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": a mapping of header names to values
            - "body": a mapping containing:
                * "user_id" (int or str convertible to int)
                * "new_email" (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.

    Notes
    -----
    - The function performs a CSRF token check.
    - It validates the email format using a simple regex.
    - If the user does not exist in `database`, the function returns False.
    """
    # 1. CSRF token validation
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract payload data
    body = req_payload.get("body", {})
    user_id_raw = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic input validation
    if user_id_raw is None or new_email is None:
        return False

    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # 4. Email format validation
    if not isinstance(new_email, str) or not _is_valid_email(new_email):
        return False

    # 5. Update the mock database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["email"] = new_email.strip()
    return True


# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    # Successful update
    payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice@newdomain.com"},
    }
    print(edit_user_email(payload))  # True
    print(database[1]["email"])      # alice@newdomain.com

    # Failure due to bad CSRF
    payload["headers"]["X-CSRF-Token"] = "wrong_token"
    print(edit_user_email(payload))  # False