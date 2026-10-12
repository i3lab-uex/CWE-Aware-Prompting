import re

# Predefined CSRF token for demonstration purposes
EXPECTED_CSRF_TOKEN = "s3cureT0ken123"

# Mock database of users: {user_id: {"email": "..."}}
database = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.org"},
}


def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address after performing CSRF protection
    and basic validation.

    Parameters:
        req (dict): Request dictionary containing headers and body data.
                    Expected keys: 'headers', 'body'.

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF protection: ensure the request includes a valid token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new email from the body
    body = req.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("email")

    if not user_id or not new_email:
        return False

    # 3. Validate that the user exists in the database
    if user_id not in database:
        return False

    # 4. Basic email format validation (RFC 5322 compliant regex is complex;
    #    we use a simple pattern for demonstration)
    email_pattern = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )
    if not email_pattern.match(new_email):
        return False

    # 5. Update the user's email
    database[user_id]["email"] = new_email

    return True