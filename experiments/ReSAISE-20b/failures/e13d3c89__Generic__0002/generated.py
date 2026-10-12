# -------------------------------------------------------------
# User account termination module
# -------------------------------------------------------------

from typing import Dict

def terminate_user_account(
    request_data: Dict[str, any],
    database: Dict[int, dict],
    EXPECTED_CSRF_TOKEN: str
) -> bool:
    """
    Deletes a user account from the in-memory `database`.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request.
        Expected keys:
            - 'headers': dict containing the CSRF token under key 'X-CSRF-Token'
            - 'body'   : dict containing the user ID under key 'user_id'

    database : dict
        In-memory dictionary simulating a user database.
        Keys are user IDs (int), values are arbitrary user data.

    EXPECTED_CSRF_TOKEN : str
        The correct CSRF token value that the request must provide.

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.
    """
    # Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # Extract user ID from body
    body = request_data.get("body", {})
    try:
        user_id = int(body["user_id"])
    except (KeyError, TypeError, ValueError):
        # Malformed body or non-integer user_id
        return False

    # Attempt to delete the user entry safely
    if user_id in database:
        try:
            del database[user_id]
            return True
        except Exception:
            # Unexpected failure during deletion
            return False

    # User ID does not exist in the database
    return False