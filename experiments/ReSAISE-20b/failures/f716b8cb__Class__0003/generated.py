import re

# Simulated global context
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def _is_valid_email(email: str) -> bool:
    """Return True if the email matches a simple RFC‑5322 pattern."""
    return EMAIL_REGEX.match(email) is not None


def modify_user_email_address(user_request: dict) -> bool:
    """
    Update a user's email address after validating the CSRF token and
    ensuring the provided data is authentic.

    Parameters
    ----------
    user_request : dict
        Expected to contain:
            - headers: dict with a 'X-CSRF-Token' key.
            - body: dict containing:
                * user_id : int
                * new_email : str

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    try:
        # 1. CSRF token verification (CWE-345 mitigation)
        headers = user_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract payload
        body = user_request.get("body", {})
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        # 3. Basic type checks
        if not isinstance(user_id, int) or not isinstance(new_email, str):
            return False

        # 4. Email format validation
        if not _is_valid_email(new_email):
            return False

        # 5. Verify user exists in the database
        if user_id not in database:
            return False

        # 6. Update the email address
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # Log exception in real application; here we just suppress it
        return False