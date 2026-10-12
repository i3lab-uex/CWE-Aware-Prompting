import re
from typing import Dict

# Simulated database and CSRF token for this example
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}$"
)


def modify_user_email_address(user_request: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input.

    Parameters
    ----------
    user_request : dict
        Incoming request containing:
            - headers: dict with a 'X-CSRF-Token' key
            - body: dict with 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if update succeeded, False otherwise.
    """
    # 1. CSRF token validation (CWE-693 mitigation)
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract and validate payload
    body = user_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError, TypeError):
        # Missing or malformed fields
        return False

    # 3. Email format validation to prevent injection attacks
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure the user exists in the database
    if user_id not in database:
        return False

    # 5. Update the email address
    database[user_id]["email"] = new_email

    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "newalice@example.com"},
    }
    print(modify_user_email_address(request))  # Expected: True
    print(database[1]["email"])                # Expected: newalice@example.com