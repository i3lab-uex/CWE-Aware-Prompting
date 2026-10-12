import re
import hmac

# Simulated database and CSRF token (would normally be configured elsewhere)
database = {}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)

def modify_user_email(req: dict) -> bool:
    """
    Modify a user's email address after verifying CSRF token and input validity.

    Parameters
    ----------
    req : dict
        Request data containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body: dict, must include 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    try:
        headers = req.get("headers", {})
        body = req.get("body", {})

        # 1. CSRF token verification using constant‑time comparison
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
            return False

        # 2. Extract and validate required fields
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        if user_id is None or new_email is None:
            return False

        # 3. Validate email format
        if not EMAIL_REGEX.match(new_email):
            return False

        # 4. Ensure the user exists in the database
        if user_id not in database:
            return False

        # 5. Update the user's email
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # In a real application, log the exception details securely
        return False