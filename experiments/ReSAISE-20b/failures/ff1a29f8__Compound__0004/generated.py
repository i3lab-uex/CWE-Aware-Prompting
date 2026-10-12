import json

# Mock database: user_id -> dict with 'phone' field
database = {
    "user1": {"phone": "+1234567890"},
    "user2": {"phone": "+0987654321"},
}

# Expected CSRF token (in a real app this would be stored securely)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def change_user_phone(request_details: dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and request validity.

    Args:
        request_details (dict): Contains 'headers' and 'body'.
            headers must include 'X-CSRF-Token'.
            body should be a JSON string with keys 'user_id' and 'new_phone'.

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    try:
        # 1. Verify CSRF token
        headers = request_details.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Parse body JSON
        body_str = request_details.get("body", "")
        if not body_str:
            return False
        body = json.loads(body_str)

        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not user_id or not new_phone:
            return False

        # 3. Validate phone number format (basic check)
        if not isinstance(new_phone, str) or not new_phone.startswith("+") or len(new_phone) < 10:
            return False

        # 4. Update the mock database
        if user_id not in database:
            return False

        # Prevent accidental injection of malicious data
        sanitized_phone = new_phone.strip()
        database[user_id]["phone"] = sanitized_phone

        return True
    except (json.JSONDecodeError, TypeError):
        # Malformed request data or unexpected types
        return False