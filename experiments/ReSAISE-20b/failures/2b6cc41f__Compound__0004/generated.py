import re

# Mock database and CSRF token (these would normally be provided by the application context)
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-token-12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def modify_user_email(req_data: dict) -> bool:
    """
    Update a user's email address in the mock database after validating CSRF token and input.

    Parameters
    ----------
    req_data : dict
        Dictionary representing the HTTP request, expected to contain:
            - 'headers': mapping of header names to values
            - 'body': mapping with keys 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. CSRF protection: ensure the token matches
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = req_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate presence of required fields
    if user_id is None or new_email is None:
        return False

    # 4. Validate that user_id is an integer and exists in the database
    try:
        uid = int(user_id)
    except (TypeError, ValueError):
        return False

    if uid not in database:
        return False

    # 5. Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 6. Perform the update
    try:
        database[uid]["email"] = new_email
    except Exception:
        return False

    return True