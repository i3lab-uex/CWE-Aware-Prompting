import re

# Sample context variables (to be provided by the caller)
database = {}  # Example: { "user1": {"phone": "1234567890"}, ... }
EXPECTED_CSRF_TOKEN = "expected_token_value"

def change_user_contact(transaction_request: dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    transaction_request : dict
        A dictionary containing 'headers' and 'body'.  The body must include:
          - 'user_id': str
          - 'new_phone': str

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Basic request validation
    if not isinstance(transaction_request, dict):
        return False

    headers = transaction_request.get("headers", {})
    body = transaction_request.get("body", {})

    # 2. CSRF token check (CWE-345 mitigation)
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user_id
    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return False

    # 4. Validate new phone number format (simple digit check, length 10-15)
    new_phone = body.get("new_phone")
    if not isinstance(new_phone, str):
        return False
    if not re.fullmatch(r"\d{10,15}", new_phone):
        return False

    # 5. Check that the user exists in the database
    if user_id not in database:
        return False

    # 6. Update the phone number safely
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Any unexpected error during the update should result in failure
        return False