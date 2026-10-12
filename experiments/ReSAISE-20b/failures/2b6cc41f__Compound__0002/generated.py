import re

# Mock database: user_id -> dict containing 'email' and other fields
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.org"}
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Simple email regex (RFC 5322 is complex; this covers common cases)
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def modify_user_email(req_data: dict) -> bool:
    """
    Update a user's email address after validating the CSRF token and input data.

    Args:
        req_data (dict): HTTP request payload. Expected keys:
            - headers: dict containing request headers.
            - body: dict containing 'user_id' (int) and 'new_email' (str).

    Returns:
        bool: True if the email was successfully updated, False otherwise.
    """
    try:
        # 1. CSRF token validation
        headers = req_data.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            # Token missing or invalid
            return False

        # 2. Extract and validate request body
        body = req_data.get("body", {})
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        if not isinstance(user_id, int) or user_id <= 0:
            return False

        if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
            return False

        # 3. Check if user exists in the mock database
        user_record = database.get(user_id)
        if not user_record:
            return False

        # 4. Update the email address
        user_record["email"] = new_email.strip()
        return True

    except Exception:
        # In a real application, log the exception. Here we simply fail gracefully.
        return False