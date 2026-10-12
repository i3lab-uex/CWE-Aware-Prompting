import re

# --- Mock context ---------------------------------------------------------
# Simulated user database: {user_id: {"email": "..."}}
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"}
}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# -------------------------------------------------------------------------

def change_user_email(query: dict) -> bool:
    """
    Update a user's email address after performing CSRF and input validation.

    Parameters
    ----------
    query : dict
        The request dictionary expected to contain:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Validate presence of headers and body
    if not isinstance(query, dict):
        raise ValueError("Query must be a dictionary.")
    headers = query.get('headers')
    body   = query.get('body')
    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("Query must contain 'headers' and 'body' dictionaries.")

    # 2. CSRF token check (CWE-693)
    csrf_token = headers.get('X-CSRF-Token')
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Reject silently to avoid leaking information
        return False

    # 3. Extract and validate user ID
    try:
        user_id = int(body.get('user_id'))
    except (TypeError, ValueError):
        return False

    # 4. Extract and validate new email
    new_email = body.get('new_email')
    if not isinstance(new_email, str):
        return False

    # Basic email regex; more thorough validation can be added if needed
    email_pattern = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    )
    if not email_pattern.match(new_email):
        return False

    # 5. Update the mock database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record['email'] = new_email
    return True