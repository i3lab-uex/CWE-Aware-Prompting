import json

# Expected CSRF token (for demonstration purposes only)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

def remove_user_account(input_request: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database` after validating
    the CSRF token and ensuring that the provided user ID exists.

    Parameters:
        input_request (dict): HTTP request representation containing
            - 'headers': dict with 'X-CSRF-Token'
            - 'body': JSON string or dict with key 'user_id'

        database (dict): In-memory user store, mapping user IDs to
            user data.

    Returns:
        bool: True if deletion succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    try:
        csrf_token = input_request.get("headers", {}).get("X-CSRF-Token")
    except AttributeError:
        # headers not a dict
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token; reject operation
        return False

    # 2. Parse body to obtain user_id
    try:
        body = input_request.get("body")
        if isinstance(body, str):
            body_data = json.loads(body)
        elif isinstance(body, dict):
            body_data = body
        else:
            return False

        user_id = body_data.get("user_id")
    except (json.JSONDecodeError, TypeError):
        return False

    if not isinstance(user_id, str) or not user_id:
        # Invalid user ID format
        return False

    # 3. Delete the user if exists
    try:
        # Use pop with default to avoid KeyError
        removed = database.pop(user_id, None)
    except Exception:
        # Any unexpected error during deletion
        return False

    return removed is not None