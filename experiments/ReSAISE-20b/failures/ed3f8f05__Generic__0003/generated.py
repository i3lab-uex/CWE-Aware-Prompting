import json
import re

# Mock database: user_id -> { "email": ... }
database = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@domain.org"}
}

# CSRF token expected by the server
EXPECTED_CSRF_TOKEN = "secure_csrf_token_value"

# Simple regex for email validation (not RFC compliant but sufficient for demo)
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def change_user_email(request_data: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": dict containing request headers.
            - "body": str or bytes containing JSON payload.

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. CSRF token validation
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Parse JSON body
    body = request_data.get("body")
    if not body:
        return False

    try:
        # body may be bytes; decode if necessary
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        payload = json.loads(body)
    except (ValueError, TypeError):
        return False

    # 3. Extract required fields
    user_id = payload.get("user_id")
    new_email = payload.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Update the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # For security, avoid storing plain text emails; in real apps use hashing or encryption if needed.
    user_record["email"] = new_email
    return True

# Example usage:
if __name__ == "__main__":
    # Simulate a request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": 1, "new_email": "new@example.com"})
    }
    print(change_user_email(req))  # Should output: True