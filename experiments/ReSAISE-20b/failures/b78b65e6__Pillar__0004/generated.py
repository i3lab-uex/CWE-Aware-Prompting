import json
import hmac

# Simulated data store and CSRF token
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"


def discard_user(req_info: dict) -> bool:
    """
    Remove a user account from the system.

    Parameters
    ----------
    req_info : dict
        HTTP request information containing headers and body.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body": '{"user_id": 42}'
            }

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # 1. CSRF token validation (constant‑time comparison)
    headers = req_info.get("headers", {})
    incoming_token = headers.get("X-CSRF-Token")
    if not incoming_token:
        return False
    if not hmac.compare_digest(incoming_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Parse the request body safely
    try:
        body = json.loads(req_info.get("body", "{}"))
        user_id = body["user_id"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return False

    # 3. Ensure user_id is an integer
    if not isinstance(user_id, int):
        return False

    # 4. Delete the user if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False


# Example usage:
if __name__ == "__main__":
    # Simulate a valid request
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": 2})
    }
    result = discard_user(request)
    print("Deleted:", result)          # Should print: Deleted: True
    print("Remaining users:", database)