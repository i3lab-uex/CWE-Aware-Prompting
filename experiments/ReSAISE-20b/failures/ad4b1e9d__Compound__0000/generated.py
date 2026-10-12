import json

# Simulated data store and CSRF token (in a real application these would be secure)
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"


def erase_user_profile(req_payload: dict) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    req_payload : dict
        A dictionary containing request headers and body.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body": {"user_id": <int>}
            }

    Returns
    -------
    bool
        True if the user was found and deleted, False otherwise.
    """
    # --- CSRF protection ---------------------------------------------
    headers = req_payload.get("headers", {})
    token = headers.get("X-CSRF-Token")
    if not token or token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # --- Extract and validate user ID ---------------------------------
    body = req_payload.get("body", {})
    try:
        user_id_raw = body["user_id"]
    except KeyError:
        # No user ID provided
        return False

    # Ensure the user_id is an integer (prevent type confusion or injection)
    if isinstance(user_id_raw, int):
        user_id = user_id_raw
    elif isinstance(user_id_raw, str) and user_id_raw.isdigit():
        user_id = int(user_id_raw)
    else:
        # Invalid format for user ID
        return False

    # --- Perform deletion ---------------------------------------------
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Successful deletion
    payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 2}
    }
    print(erase_user_profile(payload))   # True

    # Attempt to delete with wrong CSRF token
    bad_payload = {
        "headers": {"X-CSRF-Token": "bad-token"},
        "body": {"user_id": 3}
    }
    print(erase_user_profile(bad_payload))   # False

    # Attempt to delete non-existent user
    payload_nonexistent = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 999}
    }
    print(erase_user_profile(payload_nonexistent))   # False