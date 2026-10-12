import uuid
from typing import Dict, Any

# Simulated data store and CSRF token
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

def remove_account(request: Dict[str, Any]) -> bool:
    """
    Deletes a user account identified by `user_id` in the request body.

    Parameters
    ----------
    request : dict
        HTTP request representation. Expected keys:
            - 'headers': dict containing at least the CSRF token under 'X-CSRF-Token'.
            - 'body': dict containing the user ID under key 'user_id'.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Notes
    -----
    - Validates CSRF token to mitigate CWE-352.
    - Performs existence check before deletion.
    - Uses a deterministic delete operation; no side effects on unrelated keys.
    """
    # Extract headers and body safely
    headers = request.get("headers", {})
    body = request.get("body", {})

    # 1. CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or mismatched – reject request
        return False

    # 2. Retrieve user ID from body
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        # Invalid or missing user ID
        return False

    # 3. Ensure the user exists before attempting deletion
    if user_id not in database:
        # User does not exist – nothing to delete
        return False

    # 4. Perform deletion
    try:
        del database[user_id]
    except KeyError:
        # This should not happen due to the existence check,
        # but handle gracefully.
        return False

    # 5. Deletion successful
    return True


# ------------------------------------------------------------------
# Example usage (for demonstration only; not part of the required function)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Populate sample database
    uid = str(uuid.uuid4())
    database[uid] = {"name": "Alice", "email": "alice@example.com"}

    # Build a valid request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": uid}
    }

    print(f"Before deletion: {database}")
    result = remove_account(req)
    print(f"Deletion successful? {result}")
    print(f"After deletion: {database}")