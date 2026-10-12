import re

# Pre‑defined CSRF token that the server expects to receive in requests
EXPECTED_CSRF_TOKEN = "secure-csrf-token-1234"

def change_user_phone(payload: dict, database: dict) -> bool:
    """
    Update a user's phone number in the simulated database.

    Parameters
    ----------
    payload : dict
        Request dictionary containing:
            - headers: dict with 'X-CSRF-Token' key.
            - body   : dict with keys:
                * user_id (hashable, e.g. int or str)
                * phone   (string of digits)

    database : dict
        Simulated user database. Keys are user IDs; values are dicts with at least a 'phone' key.

    Returns
    -------
    bool
        True if the phone number was updated successfully; False otherwise.
    """
    try:
        # Validate CSRF token
        csrf_token = payload.get("headers", {}).get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # Extract user id and new phone number
        body = payload.get("body", {})
        user_id = body["user_id"]
        new_phone = body["phone"]

        # Basic phone validation: digits only, 7-15 characters long
        if not re.fullmatch(r"\d{7,15}", new_phone):
            return False

        # Ensure the user exists in the database
        if user_id not in database:
            return False

        # Perform the update
        database[user_id]["phone"] = new_phone
        return True

    except (KeyError, TypeError):
        # Payload structure is incorrect or database entry missing
        return False