import json

# Simulated global context (would normally be injected or imported)
database: dict = {}
EXPECTED_CSRF_TOKEN: str = "expected_token_value"

def remove_account(request: dict) -> bool:
    """
    Deletes a user account from the simulated database after verifying CSRF protection.

    Parameters
    ----------
    request : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing the CSRF token under key 'X-CSRF-Token'
            - 'body'   : str or dict containing the user ID under key 'user_id'

    Returns
    -------
    bool
        True if the account was deleted successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = request.get("headers", {})
    incoming_token = headers.get("X-CSRF-Token")
    if not incoming_token or incoming_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or mismatched – reject the request
        return False

    # 2. Extract user ID from body
    body = request.get("body")
    if body is None:
        return False

    # Body may be a JSON string or already parsed dict
    if isinstance(body, str):
        try:
            body_data = json.loads(body)
        except (ValueError, TypeError):
            return False
    elif isinstance(body, dict):
        body_data = body
    else:
        return False

    user_id = body_data.get("user_id")
    if not user_id:
        return False

    # 3. Delete the account from the database
    try:
        del database[user_id]
        return True
    except KeyError:
        # User ID does not exist in the database
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate the simulated database
    database["user123"] = {"name": "Alice"}
    request_example = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": "user123"})
    }
    result = remove_account(request_example)
    print("Account removed:", result)   # Should output: Account removed: True