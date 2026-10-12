import re

# Simulated database: user_id -> {"email": str, ...}
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token for the request
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"

# Simple regex for email validation (not exhaustive but sufficient for demo)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def update_user_email(request: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and email format.

    Args:
        request (dict): A dictionary containing:
            - headers: dict with at least 'X-CSRF-Token'
            - body: dict with keys 'user_id' (int) and 'new_email' (str)

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body parameters
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that user exists in database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # In a real scenario, log the exception
        return False

# Example usage (for testing only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"}
    }
    print(update_user_email(req))          # Should print: True
    print(database[1]["email"])            # Should show updated email