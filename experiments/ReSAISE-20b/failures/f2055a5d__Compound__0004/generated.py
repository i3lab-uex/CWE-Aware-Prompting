import logging

# Constants (would normally be defined elsewhere)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def remove_user_account(input_request: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database`.

    Parameters
    ----------
    input_request : dict
        HTTP request representation containing:
            - 'headers': dict, must include a valid CSRF token under 'X-CSRF-Token'
            - 'body': dict, must include a 'user_id' key with the ID to delete
    database : dict
        In-memory dictionary simulating user data storage.
        Keys are user IDs; values can be any user information.

    Returns
    -------
    bool
        True if the account was found and removed; False otherwise.

    Raises
    ------
    None
        All error conditions are handled gracefully and result in a False return.
    """
    # Validate request structure
    try:
        headers = input_request["headers"]
        body = input_request["body"]
    except (KeyError, TypeError):
        logging.warning("Malformed request: missing headers or body.")
        return False

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        logging.warning("CSRF token missing or invalid.")
        return False

    # Retrieve user ID to delete
    user_id = body.get("user_id")
    if not isinstance(user_id, (str, int)):
        logging.warning("Invalid or missing user_id in request body.")
        return False

    # Attempt deletion
    if user_id in database:
        del database[user_id]
        logging.info(f"User account {user_id} deleted successfully.")
        return True
    else:
        logging.warning(f"User account {user_id} not found in database.")
        return False