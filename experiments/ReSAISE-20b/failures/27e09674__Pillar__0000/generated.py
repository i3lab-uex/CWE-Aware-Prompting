import re

# Simulated database and CSRF token for the example
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Simple email validation regex (RFC 5322 simplified)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"
    r"[a-zA-Z0-9])?(?:\.[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$)"
)


def change_user_email(query: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Parameters
    ----------
    query : dict
        Dictionary containing request headers and body. Expected keys:
            - "headers": dict with key "X-CSRF-Token"
            - "body": dict with keys "user_id" (int) and "new_email" (str)

    Returns
    -------
    bool
        True if the update succeeds, False otherwise.
    """
    # Extract headers and body safely
    headers = query.get("headers") or {}
    body = query.get("body") or {}

    # 1. CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Validate presence of required fields
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if user_id is None or new_email is None:
        return False

    # 3. Ensure user_id is an integer
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return False

    # 4. Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check that user exists in the database
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error during update results in failure
        return False

    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    sample_query = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(change_user_email(sample_query))  # Expected: True
    print(database[1]["email"])            # Expected: "alice.new@example.com"