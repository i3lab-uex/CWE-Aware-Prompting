import re
from typing import Dict

# Mock database and CSRF token for demonstration purposes.
database: Dict[int, dict] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Regular expression to validate international phone numbers (simple RFC 3966-ish).
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def modify_user_phone(client_request: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        The request dictionary. Expected to contain:
            - "headers": dict with a "X-CSRF-Token" key.
            - "body": dict with keys:
                - "user_id" (int)
                - "new_phone" (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. CSRF protection: ensure token is present and matches the expected value.
    headers = client_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or invalid – reject the request.
        return False

    # 2. Extract and validate body data.
    body = client_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if user_id is None or new_phone is None:
        raise ValueError("Missing 'user_id' or 'new_phone' in request body.")

    if not isinstance(user_id, int):
        raise ValueError("'user_id' must be an integer.")

    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        raise ValueError("Invalid phone number format. Expected E.164 format.")

    # 3. Update the mock database if the user exists.
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist – cannot update.
        return False

    # 4. Perform the update (in a real scenario, this would be an SQL UPDATE).
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only):
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15551234567"},
    }
    result = modify_user_phone(request)
    print("Update successful:", result)   # Should output: True
    print("Updated record:", database[1])  # Phone should be updated