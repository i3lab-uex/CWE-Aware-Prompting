import json

# Mock database and expected CSRF token for demonstration purposes.
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "s3cureT0k3n"

def change_user_phone(request_details: dict) -> bool:
    """
    Update a user's phone number in the mock database after verifying
    CSRF token and request authenticity.

    Parameters
    ----------
    request_details : dict
        Dictionary containing HTTP request information.
        Expected keys:
            - 'headers': dict of request headers
            - 'body'   : str or dict with keys 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or invalid.
    """
    # --- 1. Validate request structure ------------------------------------
    if not isinstance(request_details, dict):
        raise ValueError("request_details must be a dictionary")

    headers = request_details.get("headers")
    body   = request_details.get("body")

    if not isinstance(headers, dict):
        raise ValueError("headers must be a dictionary")
    if body is None:
        raise ValueError("body is required")

    # --- 2. CSRF protection -----------------------------------------------
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Potential CSRF attack or missing token
        return False

    # --- 3. Parse body ----------------------------------------------------
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            raise ValueError("body must be valid JSON or a dict")

    if not isinstance(body, dict):
        raise ValueError("body must be a dictionary after parsing")

    user_id   = body.get("user_id")
    new_phone = body.get("new_phone")

    if user_id is None or new_phone is None:
        raise ValueError("user_id and new_phone are required in body")

    # Ensure user_id is an integer for database key
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise ValueError("user_id must be an integer")

    # Basic phone number validation: ensure it's a non-empty string
    if not isinstance(new_phone, str) or not new_phone.strip():
        raise ValueError("new_phone must be a non-empty string")

    # --- 4. Update database ------------------------------------------------
    user_record = database.get(user_id)
    if user_record is None:
        # User does not exist
        return False

    # Update the phone number safely
    user_record["phone"] = new_phone.strip()
    return True

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only; remove in production)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": 1, "new_phone": "+1112223333"})
    }
    print("Update succeeded:", change_user_phone(req))
    print("Updated record:", database[1])