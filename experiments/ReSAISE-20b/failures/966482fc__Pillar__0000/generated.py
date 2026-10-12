import re
import hmac

# ------------------------------------------------------------------
# Mock database and CSRF token (would normally be configured elsewhere)
# ------------------------------------------------------------------
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

EXPECTED_CSRF_TOKEN = "super-secret-token-123"

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _is_valid_email(email: str) -> bool:
    """
    Very simple email validation regex. In production, use a more robust
    validator or a dedicated library.
    """
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None

def _secure_compare(a: str, b: str) -> bool:
    """
    Constant‑time comparison to prevent timing attacks.
    """
    return hmac.compare_digest(a, b)

# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------
def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        Expected to contain:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    try:
        # 1. CSRF token validation
        headers = req.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or not _secure_compare(csrf_token, EXPECTED_CSRF_TOKEN):
            return False

        # 2. Extract body parameters
        body = req.get("body", {})
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        # 3. Basic type checks
        if not isinstance(user_id, int) or not isinstance(new_email, str):
            return False

        # 4. Validate email format
        if not _is_valid_email(new_email):
            return False

        # 5. Update the database
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Perform the update
        user_record["email"] = new_email
        return True

    except Exception:
        # Any unexpected error should result in a safe failure.
        return False