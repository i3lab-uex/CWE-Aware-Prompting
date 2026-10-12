import json
from typing import Dict

# Simulated database: mapping user_id (int) to user data
database: Dict[int, dict] = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"},
}

# Expected CSRF token value (in a real app this would be stored securely)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def delete_user_account(request: Dict) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    request : dict
        The request object containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: str or dict, expected to contain a JSON object with key 'user_id'

    Returns
    -------
    bool
        True if the user was deleted successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or incorrect
        return False

    # 2. Extract user_id from body
    body = request.get("body")
    if body is None:
        return False

    # Accept both dict and JSON string
    try:
        if isinstance(body, str):
            body_data = json.loads(body)
        else:
            body_data = body
    except (json.JSONDecodeError, TypeError):
        return False

    user_id = body_data.get("user_id")
    if not isinstance(user_id, int):
        # Reject non-integer or missing user_id
        return False

    # 3. Delete the user if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False