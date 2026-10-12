import uuid
from typing import Dict, Any

# Expected CSRF token for the application (in a real app this would be stored securely)
EXPECTED_CSRF_TOKEN = "s3cureT0k3n"

def remove_user_account(
    input_request: Dict[str, Any],
    database: Dict[uuid.UUID, dict]
) -> bool:
    """
    Delete a user account from the in-memory `database`.

    Parameters
    ----------
    input_request : dict
        HTTP request dictionary containing:
            - 'headers': mapping of header names to values (expects 'X-CSRF-Token')
            - 'body'   : mapping containing 'user_id': str or UUID
    database : dict[UUID, dict]
        In-memory user database. Keys are UUIDs.

    Returns
    -------
    bool
        True if the account was found and deleted; False otherwise.
    """
    # Validate CSRF token
    headers = input_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID from body
    body = input_request.get("body", {})
    user_id_raw = body.get("user_id")
    if not user_id_raw:
        return False

    # Convert to UUID, reject invalid format
    try:
        user_id = uuid.UUID(str(user_id_raw))
    except (ValueError, AttributeError):
        return False

    # Attempt to delete the user
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False