import json
import re

# Simulated database and CSRF token (normally these would be managed by the framework)
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"}
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Regular expression for a basic email validation (RFC 5322 compliant is complex; this covers most cases)
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$")


def modify_user_email_address(user_request: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Args:
        user_request (dict): Incoming request containing headers and a JSON body.
            Expected keys:
                - "headers": dict with at least the 'X-CSRF-Token' key.
                - "body": str or dict representing JSON data with 'user_id' and 'new_email'.

    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    # 1. Verify CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token; do not proceed
        return False

    # 2. Parse body (ensure it is JSON)
    body = user_request.get("body")
    if isinstance(body, str):
        try:
            body_data = json.loads(body)
        except json.JSONDecodeError:
            return False
    elif isinstance(body, dict):
        body_data = body
    else:
        return False

    # 3. Extract required fields
    user_id = body_data.get("user_id")
    new_email = body_data.get("new_email")

    if not isinstance(user_id, int) or user_id <= 0:
        return False
    if not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Ensure user exists in the database
    if user_id not in database:
        return False

    # 6. Update the email (simulate a secure update)
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error during update should fail gracefully
        return False

    return True