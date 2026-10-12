import json
from typing import Dict, Any

# Simulated data store and CSRF token
database: Dict[str, Any] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"


def erase_user_profile(req_payload: Dict[str, Any]) -> bool:
    """
    Deletes a user profile from the in-memory `database` if the request
    contains a valid CSRF token and a legitimate user ID.

    Parameters
    ----------
    req_payload : dict
        A dictionary representing the HTTP request. It must contain:
            - headers: a dict with 'X-CSRF-Token' key
            - body: a JSON string or dict containing the key 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Notes
    -----
    - The function performs strict type and value checks to mitigate CWE-345.
    - It does not reveal whether the user existed or not to avoid leaking
      information.
    """
    # 1. Verify headers and CSRF token
    try:
        headers = req_payload["headers"]
        csrf_token = headers.get("X-CSRF-Token")
    except (KeyError, AttributeError):
        return False

    if not isinstance(csrf_token, str) or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate user_id from body
    try:
        body = req_payload["body"]
        if isinstance(body, str):
            # Assume JSON string
            body = json.loads(body)
    except (KeyError, json.JSONDecodeError):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id.strip():
        return False

    # 3. Attempt deletion
    # Use pop with default to avoid KeyError; result is None if not found
    deleted = database.pop(user_id, None)

    # 4. Return True only if a record was actually removed
    return deleted is not None


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate the database
    database["alice"] = {"email": "alice@example.com"}
    database["bob"] = {"email": "bob@example.com"}

    # Construct a request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": "alice"})
    }

    print(erase_user_profile(req))  # Expected: True
    print(database)                 # alice should be removed