import re

# Mock database and CSRF token constant
database: dict[int, dict] = {}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def remove_user_account(req: dict) -> bool:
    """
    Removes a user account from the in-memory `database` using the
    user ID supplied in the request.

    Parameters
    ----------
    req : dict
        HTTP request representation. Expected keys:
            - 'headers': mapping of header names to values.
            - 'body': JSON-like dict containing a key `user_id`.

    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.
    """
    try:
        # 1. Verify CSRF token
        headers = req.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate user ID
        body = req.get("body", {})
        raw_user_id = body.get("user_id")
        if not isinstance(raw_user_id, int):
            # Reject non-integer or missing IDs
            return False

        # 3. Ensure user exists before attempting deletion
        if raw_user_id not in database:
            return False

        # 4. Delete the user record
        del database[raw_user_id]
        return True

    except Exception:
        # In production, log the exception. Here we silently fail.
        return False