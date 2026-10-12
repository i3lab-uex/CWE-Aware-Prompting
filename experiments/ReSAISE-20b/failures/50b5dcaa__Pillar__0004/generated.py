import re
from typing import Dict

# Mock database and CSRF token for demonstration purposes
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a simple but reasonably strict email validation
EMAIL_REGEX = re.compile(
    r"^(?P<local>[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+)@(?P<domain>[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$"
)


def _is_valid_email(email: str) -> bool:
    """
    Validate the email address format using a regex.
    Returns True if the email matches the pattern, otherwise False.
    """
    return bool(EMAIL_REGEX.match(email))


def edit_user_email(req_payload: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and email format.

    Parameters
    ----------
    req_payload : dict
        A dictionary representing the HTTP request. Expected keys:
            - 'headers': dict containing at least a 'X-CSRF-Token' entry.
            - 'body': dict containing:
                * 'user_id' (int)
                * 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Notes
    -----
    - The function performs a strict CSRF token check before any other action.
    - Email format is validated with a regex to mitigate injection and spam.
    - The mock database update occurs only if the user exists and the new email is valid.
    """
    # 1. CSRF protection
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token mismatch – reject the request
        return False

    # 2. Extract body data
    body = req_payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate input types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 5. Update the mock database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["email"] = new_email.strip()
    return True


# Example usage (would normally be in a test or application code)
if __name__ == "__main__":
    payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(edit_user_email(payload))  # Expected: True
    print(database[1]["email"])      # Expected: alice.new@example.com