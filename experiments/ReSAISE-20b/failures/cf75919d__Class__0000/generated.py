import json

# Simulated database and expected CSRF token (in a real app these would be stored securely)
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def delete_user_account(request: dict) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    request : dict
        The incoming request containing headers and a JSON body with the user ID.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body": "{\"user_id\": 42}"
            }

    Returns
    -------
    bool
        True if the user was deleted successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or incorrect – reject the operation
        return False

    # 2. Parse and validate body
    try:
        body = request.get("body", "{}")
        payload = json.loads(body)
    except (ValueError, TypeError):
        # Malformed JSON
        return False

    user_id = payload.get("user_id")
    if not isinstance(user_id, int):
        # User ID must be an integer
        return False

    # 3. Perform deletion if user exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False