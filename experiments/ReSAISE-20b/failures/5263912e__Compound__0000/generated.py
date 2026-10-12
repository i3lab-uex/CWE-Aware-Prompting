import json

# Constants and mock database for demonstration purposes
EXPECTED_CSRF_TOKEN = "s3cureT0ken123"
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}

def remove_user_account(req: dict) -> bool:
    """
    Remove a user account identified by the `user_id` in the request body.

    Args:
        req (dict): Representation of an HTTP request. Expected keys are:
            - 'headers': dict containing at least the 'X-CSRF-Token' header.
            - 'body': JSON string or dict containing a 'user_id'.

    Returns:
        bool: True if the account was removed, False otherwise.

    Raises:
        ValueError: If required data is missing or malformed.
    """
    # 1. Verify CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF protection failed
        return False

    # 2. Parse body for user_id
    body = req.get("body")
    if isinstance(body, str):
        try:
            body_data = json.loads(body)
        except json.JSONDecodeError:
            return False
    elif isinstance(body, dict):
        body_data = body
    else:
        return False

    user_id_raw = body_data.get("user_id")
    if user_id_raw is None:
        return False

    # 3. Ensure user_id is an integer and exists in the database
    try:
        user_id = int(user_id_raw)
    except (ValueError, TypeError):
        return False

    # 4. Delete the user record if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False