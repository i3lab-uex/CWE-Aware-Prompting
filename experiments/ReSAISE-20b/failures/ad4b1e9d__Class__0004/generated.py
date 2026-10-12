import hmac
from typing import Dict

# Simulated data store and CSRF token (these would normally be provided by the framework)
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN: str = "known_csrf_token_value"

def erase_user_profile(req_payload: Dict) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    req_payload : dict
        Dictionary representing an HTTP request, expected to contain:
            - 'headers': mapping of header names to values
            - 'body'   : dictionary with at least the key 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Notes
    -----
    - The function performs a constant‑time comparison of the CSRF token to mitigate timing attacks.
    - It validates that 'user_id' is a non‑empty string and exists in the database before deletion.
    - Any failure (missing fields, CSRF mismatch, non‑existent user) results in a False return value.
    """
    try:
        # 1. Extract headers and body safely
        headers = req_payload.get("headers", {})
        body = req_payload.get("body", {})

        # 2. Verify CSRF token
        incoming_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
        if not incoming_token:
            return False
        # Constant‑time comparison to avoid timing attacks
        if not hmac.compare_digest(incoming_token, EXPECTED_CSRF_TOKEN):
            return False

        # 3. Extract and validate user ID
        user_id = body.get("user_id")
        if not isinstance(user_id, str) or not user_id.strip():
            return False

        # 4. Delete the user if it exists
        if user_id in database:
            del database[user_id]
            return True

    except Exception:
        # Log exception in real code; for this example we simply swallow it
        pass

    return False