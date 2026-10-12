import re

# Mock database: mapping user_id (int) -> dict with 'email' field
database = {
    1: {'email': 'alice@example.com'},
    2: {'email': 'bob@example.org'}
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        Request dictionary expected to contain:
            - 'headers': dict with a 'X-CSRF-Token' key.
            - 'body': dict with keys 'user_id' (int) and 'new_email' (str).

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req.get('headers', {})
    csrf_token = headers.get('X-CSRF-Token')
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = req.get('body', {})
    try:
        user_id = int(body['user_id'])
        new_email = body['new_email']
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Verify user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update
    user_record['email'] = new_email
    return True