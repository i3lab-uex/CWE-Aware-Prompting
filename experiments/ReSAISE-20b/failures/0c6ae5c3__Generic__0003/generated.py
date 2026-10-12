import json

# Predefined CSRF token used for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

def erase_user_account(request_info: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database` based on the provided
    request information. The function performs CSRF validation and ensures that
    the user ID is present in the request body before attempting deletion.

    Parameters:
        request_info (dict): A dictionary representing an HTTP request. It
            should contain a 'headers' key with the CSRF token under
            'X-CSRF-Token', and a 'body' key containing JSON data with the
            user ID to delete.
        database (dict): In-memory dictionary simulating a user database.
            Keys are user IDs, values are arbitrary user data.

    Returns:
        bool: True if the account was found and deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate user ID from request body
    body = request_info.get("body")
    if body is None:
        return False

    # Body may be a dict or a JSON string
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 3. Perform deletion in a thread-safe manner
    # (In real applications, use proper locking or transactional DB ops.)
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False