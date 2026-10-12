import re

# Simulated database and expected CSRF token for demonstration purposes.
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}
EXPECTED_CSRF_TOKEN = "secure-token-12345"

# Regular expression for a basic international phone number validation.
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def _validate_csrf_token(request: dict) -> bool:
    """Validate the CSRF token present in request headers."""
    try:
        token = request["headers"].get("X-CSRF-Token", "")
    except AttributeError:
        return False
    return token == EXPECTED_CSRF_TOKEN

def _validate_phone_number(phone: str) -> bool:
    """Validate that the phone number matches the expected pattern."""
    return isinstance(phone, str) and bool(PHONE_REGEX.fullmatch(phone))

def update_user_phone(request: dict) -> bool:
    """
    Update the phone number for a user in the simulated database.

    Parameters
    ----------
    request : dict
        The incoming request containing headers and body.
        Expected keys:
            - 'headers': dict with key 'X-CSRF-Token'
            - 'body'   : dict with keys 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    * CSRF token validation is performed to mitigate CWE-693.
    * Phone number format is validated with a regex.
    * The function performs no I/O; it operates purely on the provided data structures.
    """
    # 1. CSRF protection
    if not _validate_csrf_token(request):
        return False

    # 2. Extract and validate request body
    try:
        body = request["body"]
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"])
    except (KeyError, TypeError, ValueError):
        return False

    # 3. Validate phone number format
    if not _validate_phone_number(new_phone):
        return False

    # 4. Check user existence
    if user_id not in database:
        return False

    # 5. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
    except Exception:  # Catch unexpected mutation errors
        return False

    return True