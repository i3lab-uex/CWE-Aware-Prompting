import re

# Preconfigured CSRF token used for request validation
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Sample in‑memory user database
# Format: {user_id (int): {"phone": str, ...}}
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}


def alter_user_phone(service_request: dict) -> bool:
    """
    Update a user's phone number in the database after validating the request.

    Parameters
    ----------
    service_request : dict
        Expected to contain:
            - headers: a mapping that includes the 'X-CSRF-Token' key.
            - body: a dict with keys:
                * "user_id" (int or convertible to int)
                * "new_phone" (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # --- 1. Validate CSRF token ---------------------------------------------
    headers = service_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # --- 2. Extract body and validate required fields -----------------------
    body = service_request.get("body", {})
    try:
        user_id_raw = body["user_id"]
        new_phone = body["new_phone"]
    except KeyError:
        return False

    # Convert user_id to int safely
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # --- 3. Validate phone number format ------------------------------------
    # Simple E.164 validation: + followed by 10-15 digits
    if not isinstance(new_phone, str):
        return False
    phone_pattern = re.compile(r"^\+\d{10,15}$")
    if not phone_pattern.match(new_phone):
        return False

    # --- 4. Update the database ---------------------------------------------
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Prevent accidental overwrite of other fields
    user_record["phone"] = new_phone
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15559876543"},
    }
    print(alter_user_phone(req))  # Expected: True
    print(database[1]["phone"])   # Updated phone number