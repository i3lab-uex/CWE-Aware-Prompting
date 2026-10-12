import re

# Mock database: user_id -> { 'email': str, ... }
database = {}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure_token_123"

def change_user_email(request_data: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing at least the 'X-CSRF-Token' header.
            - 'body': dict with keys:
                * 'user_id': int or str identifying the user.
                * 'new_email': str containing the new email address.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF protection: validate token
    headers = request_data.get('headers', {})
    csrf_token = headers.get('X-CSRF-Token')
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = request_data.get('body', {})
    user_id = body.get('user_id')
    new_email = body.get('new_email')

    # 3. Validate input presence
    if user_id is None or new_email is None:
        return False

    # 4. Validate email format (simple RFC-5322 subset)
    email_regex = re.compile(
        r"(^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"
        r"@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$)"
    )
    if not email_regex.match(new_email):
        return False

    # 5. Ensure user exists in the mock database
    if str(user_id) not in map(str, database.keys()):
        return False

    # 6. Perform the update
    try:
        database[str(user_id)]['email'] = new_email
        return True
    except Exception:
        # Any unexpected error (e.g., type errors) results in failure
        return False