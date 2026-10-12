import json

# Simulated database: mapping user_id -> dict with 'email' key.
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"


def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and request body.

    Parameters
    ----------
    new_request : dict
        The incoming HTTP-like request. Expected keys:
            - 'headers': dict containing at least 'X-CSRF-Token'
            - 'body': str (JSON) with fields:
                * 'user_id' : int
                * 'new_email': str

    Returns
    -------
    bool
        True if the email was updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = new_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Parse request body
    body = new_request.get("body")
    if not isinstance(body, str):
        return False
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return False

    user_id = data.get("user_id")
    new_email = data.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Basic email format check
    if "@" not in new_email or "." not in new_email.split("@")[-1]:
        return False

    # 4. Update the simulated database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Overwrite the email address
    user_record["email"] = new_email.strip()
    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": 1, "new_email": "alice.new@example.com"})
    }
    print(change_user_email(request))  # Should output: True
    print(database[1]["email"])        # Should show updated email