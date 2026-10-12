import re

# Simulated database: user_id -> {"email": str, ...}
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token for this example
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple but reasonable email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,}$"
)

def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Parameters
    ----------
    new_request : dict
        The incoming request containing headers and a body with keys:
            - 'csrf_token': CSRF token string
            - 'user_id'   : int or str convertible to int
            - 'new_email' : string email address

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or new_request.get("csrf_token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body data
    body = new_request.get("body", {})
    user_id_raw = body.get("user_id")
    new_email = body.get("new_email")

    if user_id_raw is None or new_email is None:
        return False

    # Ensure user_id is an integer
    try:
        user_id = int(user_id_raw)
    except (ValueError, TypeError):
        return False

    # Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 3. Check that the user exists in the database
    if user_id not in database:
        return False

    # 4. Update the email
    database[user_id]["email"] = new_email
    return True

# Example usage:
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"}
    }
    print(change_user_email(request))  # Should output: True