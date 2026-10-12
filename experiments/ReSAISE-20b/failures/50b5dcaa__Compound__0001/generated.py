import re

# Mock database and CSRF token for demonstration purposes.
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Simple email regex (RFC 5322 is complex; this covers most common cases).
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$)"
)

def edit_user_email(req_payload: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input.

    Args:
        req_payload (dict): Dictionary representing the HTTP request.
            Expected keys:
                - 'headers': dict containing at least 'X-CSRF-Token'
                - 'body': dict with keys:
                    * 'user_id' (int)
                    * 'new_email' (str)

    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate request body
    body = req_payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure user exists in the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    user_record["email"] = new_email
    return True

# Example usage (for testing only):
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(edit_user_email(request))  # Expected: True
    print(database[1]["email"])      # Updated email