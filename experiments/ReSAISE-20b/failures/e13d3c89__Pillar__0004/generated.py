import json

# Predefined CSRF token for the application
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

def terminate_user_account(request_data: dict, database: dict) -> bool:
    """
    Delete a user account from the in-memory `database` if the request is valid.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': a dictionary containing the CSRF token under 'X-CSRF-Token'
            - 'body': a JSON string or dictionary containing the user ID under key 'user_id'

    database : dict
        In-memory dictionary simulating a user database. Keys are user IDs.

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.
    """
    # --- 1. Validate request structure ---------------------------------------
    if not isinstance(request_data, dict):
        return False

    headers = request_data.get("headers", {})
    body = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, (dict, str)):
        return False

    # --- 2. Verify CSRF token -----------------------------------------------
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # --- 3. Parse body and extract user_id ---------------------------------
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return False

    # --- 4. Delete the user from the database --------------------------------
    if user_id in database:
        # Using `pop` ensures the key is removed safely
        database.pop(user_id, None)
        return True

    # User ID not found in the database
    return False