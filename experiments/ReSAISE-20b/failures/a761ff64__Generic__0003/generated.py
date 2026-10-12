import re

# Simulated database and CSRF token for the application
database: dict[int, dict] = {
    1: {"name": "Alice", "phone": "123-456-7890"},
    2: {"name": "Bob",   "phone": "987-654-3210"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token"

def _is_valid_phone(phone: str) -> bool:
    """
    Very basic phone number validation.
    Accepts digits, spaces, dashes, parentheses and a leading plus sign.
    """
    pattern = r"^\+?[0-9\s\-\(\)]{7,20}$"
    return bool(re.fullmatch(pattern, phone))

def alter_user_phone(input: dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    input : dict
        Must contain:
            headers: dict with key 'X-CSRF-Token'
            body   : dict with keys 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated,
        False otherwise.

    Raises
    ------
    KeyError
        If required keys are missing in the input.
    ValueError
        If the CSRF token is invalid or phone number format is wrong.
    """
    # Validate presence of required sections
    if "headers" not in input or "body" not in input:
        raise KeyError("Input must contain 'headers' and 'body' keys")

    headers = input["headers"]
    body   = input["body"]

    # CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        raise ValueError("Invalid CSRF token")

    # Extract user id and new phone number
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError, TypeError) as exc:
        raise KeyError("Missing or invalid 'user_id'/'new_phone'") from exc

    # Validate phone format
    if not _is_valid_phone(new_phone):
        raise ValueError("Invalid phone number format")

    # Check that the user exists
    if user_id not in database:
        return False

    # Perform the update
    database[user_id]["phone"] = new_phone
    return True