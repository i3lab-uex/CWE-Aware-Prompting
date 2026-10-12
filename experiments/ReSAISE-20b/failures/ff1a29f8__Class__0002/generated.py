import re
import json

# Mock database and expected CSRF token (normally these would be provided by the framework)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "securetoken123"

# Regular expression for validating international phone numbers (basic check)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def change_user_phone(request_details: dict) -> bool:
    """
    Update a user's phone number after verifying request authenticity.

    Parameters
    ----------
    request_details : dict
        Dictionary containing request headers and body. Expected keys:
            - "headers": dict of HTTP headers
            - "body"   : JSON string with keys "user_id" and "new_phone"

    Returns
    -------
    bool
        True if the update succeeds, False otherwise.
    """
    try:
        # 1. Verify CSRF token
        headers = request_details.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
            # Invalid or missing CSRF token
            return False

        # 2. Verify Content-Type header (ensuring JSON payload)
        content_type = headers.get("Content-Type", "")
        if "application/json" not in content_type.lower():
            return False

        # 3. Parse JSON body
        raw_body = request_details.get("body", "")
        if not raw_body:
            return False
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError:
            return False

        # 4. Extract and validate user ID
        user_id = body.get("user_id")
        if not isinstance(user_id, int) or user_id not in database:
            return False

        # 5. Validate new phone number format
        new_phone = body.get("new_phone")
        if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
            return False

        # 6. Perform the update
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # Any unexpected error should result in a safe failure
        return False