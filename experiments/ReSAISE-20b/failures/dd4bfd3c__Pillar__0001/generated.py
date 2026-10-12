import re

# Simulated database and expected CSRF token
database = {
    1: {"name": "Alice", "phone": "555-0100"},
    2: {"name": "Bob",   "phone": "555-0200"},
}
EXPECTED_CSRF_TOKEN = "secure-token-12345"

# Regular expression for a basic phone number format (e.g., 555-0100 or +1-800-555-0199)
PHONE_REGEX = re.compile(r'^\+?[\d\s\-()]{7,15}$')

def update_user_phone(request: dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input.

    Args:
        request (dict): Dictionary containing 'headers' and 'body'.
            Expected keys in body: 'user_id' (int), 'new_phone' (str).

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract and validate request body
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or user_id not in database:
        # Invalid or unknown user
        return False

    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone.strip()):
        # Invalid phone format
        return False

    # 3. Perform the update (simulate atomic operation)
    try:
        database[user_id]["phone"] = new_phone.strip()
        return True
    except Exception:
        # Log exception in real application; here we simply fail gracefully.
        return False