import logging

# Configure basic logger (in real applications this should be more robust)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Simulated data store
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}

# Expected CSRF token for demonstration purposes
EXPECTED_CSRF_TOKEN = "s3cureT0k3n"

def remove_account(request: dict) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    request : dict
        HTTP request representation. Expected to contain:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict, must include 'user_id' (int)

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        logging.warning("CSRF token mismatch or missing")
        return False

    # 2. Validate request body and user_id
    body = request.get("body", {})
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        logging.warning(f"Invalid or missing user_id: {user_id!r}")
        return False

    # 3. Attempt to delete the user
    if user_id in database:
        del database[user_id]
        logging.info(f"User {user_id} deleted successfully")
        return True
    else:
        logging.warning(f"Attempted to delete non-existent user_id: {user_id}")
        return False