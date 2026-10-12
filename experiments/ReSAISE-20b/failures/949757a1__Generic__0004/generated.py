import json

# Sample database and CSRF token (would normally be external configuration)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

def change_user_contact(transaction_request: dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    transaction_request : dict
        Must contain a 'headers' mapping with a 'X-CSRF-Token' key and a
        'body' string that is JSON encoded. The body should include:
            {
                "user_id": int,
                "new_phone": str
            }

    Returns
    -------
    bool
        True if the phone number was updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = transaction_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Parse the body
    body = transaction_request.get("body")
    if not isinstance(body, str):
        return False
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return False

    # 3. Extract required fields
    user_id = data.get("user_id")
    new_phone = data.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Basic validation of phone format (simple check)
    if not new_phone.startswith("+") or len(new_phone) < 7:
        return False

    # Update the phone number
    user_record["phone"] = new_phone
    return True