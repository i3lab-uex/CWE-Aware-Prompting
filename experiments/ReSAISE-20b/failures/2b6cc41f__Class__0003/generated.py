import re

# Mock database and CSRF token used for validation
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z]{2,})+$)"
)

def modify_user_email(req_data: dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and validating
    the new email format.

    Parameters:
        req_data (dict): HTTP request data containing headers and body.
                         Expected keys: 'headers', 'body'.

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new email from body
    body = req_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or user_id <= 0:
        return False
    if not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that the user exists in the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # In a real scenario, log the exception for audit purposes
        return False