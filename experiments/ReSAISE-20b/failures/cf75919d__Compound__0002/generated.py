import json

# Simulated database of users: user_id -> user data
database = {
    "1": {"name": "Alice"},
    "2": {"name": "Bob"},
    "3": {"name": "Charlie"}
}

# Expected CSRF token (in a real app this would be stored per session)
EXPECTED_CSRF_TOKEN = "secure_random_token_123"

def delete_user_account(request: dict) -> bool:
    """
    Deletes a user account identified by the 'user_id' in the request body.
    
    The function performs CSRF protection by validating a token included
    in the request headers. It also ensures that the user ID is present
    and exists in the database before deletion.
    
    Parameters:
        request (dict): The request object containing:
            - headers: dict, may contain 'X-CSRF-Token'
            - body: str or bytes (JSON), must include "user_id"
    
    Returns:
        bool: True if deletion succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid
        return False

    # 2. Parse body to extract user_id
    body = request.get("body")
    if body is None:
        return False

    # Body can be a JSON string or bytes
    if isinstance(body, (bytes, bytearray)):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError:
            return False

    try:
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False

    user_id = data.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 3. Verify user exists
    if user_id not in database:
        return False

    # 4. Delete the user
    try:
        del database[user_id]
    except KeyError:
        return False

    return True