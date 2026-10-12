import re

# Mock database and CSRF token for demonstration purposes
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Simple email validation regex (RFC 5322 compliant is complex, this covers most common cases)
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r"@([A-Za-z0-9](-?[A-Za-z0-9])*\.)+[A-Za-z]{2,}$)"
)


def modify_user_email(req_data: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_data : dict
        A dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing at least the 'X-CSRF-Token' header.
            - 'body': dict containing:
                - 'user_id': int
                - 'new_email': str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Notes
    -----
    - CSRF protection: The function checks that the 'X-CSRF-Token' header matches
      EXPECTED_CSRF_TOKEN.
    - Basic email format validation is performed using a regex.
    - The function updates the `database` global variable directly.
    """
    # 1. CSRF token validation
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = req_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate input types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check user existence
    if user_id not in database:
        return False

    # 6. Update the email
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # In a real-world scenario, log the exception details.
        return False