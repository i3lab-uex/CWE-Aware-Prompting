import re

# Mock database and CSRF token for the example
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Simple email validation regex (RFC 5322 compliant but simplified)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"
    r"[a-zA-Z0-9])?(?:\.[a-zA-Z]{2,})+$)"
)

def modify_user_email(req_data: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input.

    Parameters
    ----------
    req_data : dict
        Dictionary containing HTTP request data. Expected keys:
            - 'headers': dict, must contain 'X-CSRF-Token'
            - 'body': dict, must contain 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid
        return False

    # 2. Extract body data
    body = req_data.get("body", {})
    user_id_raw = body.get("user_id")
    new_email_raw = body.get("new_email")

    # 3. Validate presence and types
    if user_id_raw is None or new_email_raw is None:
        return False

    try:
        user_id = int(user_id_raw)
    except (ValueError, TypeError):
        return False

    if not isinstance(new_email_raw, str):
        return False
    new_email = new_email_raw.strip()

    # 4. Email format validation
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check user existence
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # 6. Update email in the mock database
    try:
        user_record["email"] = new_email
    except Exception:
        # In case of any unexpected error during assignment
        return False

    return True