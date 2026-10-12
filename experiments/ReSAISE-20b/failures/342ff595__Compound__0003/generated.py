import re
from typing import Dict

# Mock in‑memory database: user_id (str) -> user record (dict)
database: Dict[str, dict] = {}

# Constant representing the correct CSRF token
EXPECTED_CSRF_TOKEN: str = "s3cUrE-t0k3n-1234"

# Regular expression to validate user IDs (alphanumeric, 1‑64 chars)
USER_ID_RE = re.compile(r"^[A-Za-z0-9]{1,64}$")


def remove_user_profile(request_data: Dict) -> bool:
    """
    Remove a user profile from the in‑memory database.

    Parameters
    ----------
    request_data : dict
        Representation of an HTTP request. Expected keys:
            - 'headers': dict containing at least 'X-CSRF-Token'
            - 'body'   : dict containing the key 'user_id'

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.

    Raises
    ------
    ValueError
        If required data is missing or invalid.
    """
    # 1. CSRF protection: ensure token matches expected value
    try:
        headers = request_data["headers"]
        csrf_token = headers.get("X-CSRF-Token", "")
    except KeyError:
        raise ValueError("Missing request headers")

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Potential CSRF attack – reject silently
        return False

    # 2. Extract and validate the user ID from the request body
    try:
        body = request_data["body"]
        raw_user_id = body.get("user_id", "")
    except KeyError:
        raise ValueError("Missing request body")

    if not isinstance(raw_user_id, str) or not USER_ID_RE.match(raw_user_id):
        raise ValueError("Invalid user ID format")

    # 3. Perform the deletion in a thread‑safe manner
    # (In real systems, use database transactions or locks)
    if raw_user_id in database:
        del database[raw_user_id]
        return True

    # User not found – treat as non‑error (idempotent delete)
    return False