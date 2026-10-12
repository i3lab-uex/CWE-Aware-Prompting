import json

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token"

def remove_user_data(data: dict, database: dict) -> bool:
    """
    Remove a user from the in-memory `database` using the user ID supplied
    in the HTTP request body. The function validates a CSRF token to protect
    against cross‑site request forgery.

    Parameters:
        data (dict): A representation of an HTTP request. It must contain
                     a 'headers' key with the CSRF token and a 'body'
                     containing JSON with the field 'user_id'.
        database (dict): The in‑memory user store. Keys are user IDs and
                         values are user data dictionaries.

    Returns:
        bool: True if the user was removed, False otherwise.
    """
    # 1. Validate CSRF token
    headers = data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract user_id from request body
    try:
        body = data.get("body", "")
        if isinstance(body, bytes):
            body = body.decode()
        payload = json.loads(body)
    except (json.JSONDecodeError, AttributeError):
        return False

    user_id = payload.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return False

    # 3. Remove the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False