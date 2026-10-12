import re

# Simulated database and expected CSRF token
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-token-12345"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def update_user_email(request: dict) -> bool:
    """
    Update the email address of a user.

    Parameters
    ----------
    request : dict
        Expected keys:
            - 'headers': dict containing the CSRF token under key 'X-CSRF-Token'
            - 'body': dict containing:
                * 'user_id' (int)
                * 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Validate request structure
    headers = request.get("headers", {})
    body = request.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token validation (CWE-693)
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 4. Validate new email format
    new_email = body.get("new_email")
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 5. Perform the update if user exists
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # Update email
    user_record["email"] = new_email
    return True