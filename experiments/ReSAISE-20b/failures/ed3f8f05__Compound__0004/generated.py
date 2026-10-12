import re

# Mock database and CSRF token for demonstration purposes.
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for basic email validation.
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r"@([A-Za-z0-9](-?[A-Za-z0-9])*\.)+[A-Za-z]{2,}$)"
)

def _validate_csrf(token: str) -> bool:
    """Check that the provided CSRF token matches the expected one."""
    return token == EXPECTED_CSRF_TOKEN

def _validate_email(email: str) -> bool:
    """Return True if email matches a simple RFC‑5322 compatible pattern."""
    return EMAIL_REGEX.match(email) is not None

def change_user_email(request_data: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    request_data : dict
        Must contain:
            - 'headers': dict with at least the key 'X-CSRF-Token'.
            - 'body': dict with keys:
                * 'user_id' : int
                * 'new_email': str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF protection
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not _validate_csrf(csrf_token):
        return False

    # 2. Extract and validate request body
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or user_id <= 0:
        return False
    if not isinstance(new_email, str) or not _validate_email(new_email):
        return False

    # 3. Update the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Ensure the new email is different to avoid unnecessary writes
    if user_record.get("email") == new_email:
        return True

    # Perform the update
    user_record["email"] = new_email
    return True