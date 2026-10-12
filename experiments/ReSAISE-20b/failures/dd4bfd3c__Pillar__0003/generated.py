import hmac
import re

# Simulated database: user_id -> dict with 'phone' field
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Expected CSRF token (in a real app this would be stored in session)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def update_user_phone(request: dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and input validity.

    Args:
        request (dict): Should contain:
            - headers: dict, may include 'X-CSRF-Token'
            - body: dict with keys:
                * 'user_id': int
                * 'new_phone': str

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    # 1. Verify CSRF token using constant-time comparison
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract and validate body parameters
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or user_id <= 0:
        return False
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 3. Ensure user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 4. Perform the update
    try:
        user_record["phone"] = new_phone
        return True
    except Exception:
        # Log exception in real application; here we simply fail safely
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": "secure_csrf_token_123"},
        "body": {"user_id": 1, "new_phone": "+15551234567"},
    }
    print(update_user_phone(req))  # Expected: True