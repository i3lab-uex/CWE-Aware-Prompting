import re

# Simulated database and CSRF token
database: dict[int, dict] = {}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

def alter_user_phone(input: dict) -> bool:
    """
    Update a user's phone number in the simulated database.

    Parameters
    ----------
    input : dict
        Expected keys:
            - headers: dict containing a 'csrf-token' key.
            - body: dict with keys:
                * user_id : int
                * new_phone : str

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or the phone number is invalid.
    """
    # Validate CSRF token
    headers = input.get("headers", {})
    csrf_token = headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract body
    body = input.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if user_id is None or new_phone is None:
        return False

    # Basic phone validation: 10-15 digits, optional + at start
    if not re.fullmatch(r"\+?\d{10,15}", new_phone):
        return False

    # Ensure user exists
    if user_id not in database:
        return False

    # Update phone number
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Log the exception in real application; here we just fail silently.
        return False