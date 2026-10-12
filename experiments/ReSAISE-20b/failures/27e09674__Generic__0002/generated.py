import re

# Predefined CSRF token for protection
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Mock database: user_id -> dict containing 'email'
database = {
    "1": {"email": "old@example.com"},
    "2": {"email": "another@domain.com"},
}


def change_user_email(query: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    query : dict
        Dictionary containing request data. Expected keys:
            - 'headers': dict, may contain 'X-CSRF-Token'
            - 'body': dict with keys:
                - 'user_id' (str)
                - 'new_email' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or CSRF token is invalid.
    """
    # 1. Validate CSRF token
    headers = query.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = query.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 3. Validate email format (simple regex)
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", new_email):
        return False

    # 4. Update the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Simulate a safe update (e.g., atomic operation in real DB)
    user_record["email"] = new_email
    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    # Successful update
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "1", "new_email": "new@example.com"},
    }
    print(change_user_email(request))  # True
    print(database["1"]["email"])       # new@example.com

    # Failure due to wrong CSRF token
    bad_request = {
        "headers": {"X-CSRF-Token": "bad-token"},
        "body": {"user_id": "1", "new_email": "another@example.com"},
    }
    print(change_user_email(bad_request))  # False