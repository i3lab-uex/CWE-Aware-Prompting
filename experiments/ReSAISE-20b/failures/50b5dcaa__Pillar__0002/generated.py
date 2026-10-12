import re
import hmac

# Mock database: user_id -> {'email': str, ...}
database = {}

# Expected CSRF token
EXPECTED_CSRF_TOKEN = "super_secret_csrf_token_value"

# Regular expression for a very simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$"
)

def _validate_csrf_token(token: str) -> bool:
    """
    Compare CSRF tokens using a constant‑time comparison to mitigate timing attacks.
    """
    if token is None:
        return False
    # hmac.compare_digest performs a constant‑time comparison
    return hmac.compare_digest(token, EXPECTED_CSRF_TOKEN)

def _is_valid_email(email: str) -> bool:
    """
    Basic email format validation. Not a full RFC 5322 parser but sufficient for demo.
    """
    return bool(EMAIL_REGEX.fullmatch(email))

def edit_user_email(req_payload: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_payload : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing at least the CSRF token under
              'X-CSRF-Token' or 'csrf-token'.
            - 'body': dict containing:
                * 'user_id' (int or str)
                * 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. CSRF protection
    headers = req_payload.get("headers", {})
    csrf_token = (
        headers.get("X-CSRF-Token")
        or headers.get("csrf-token")
        or ""
    )
    if not _validate_csrf_token(csrf_token):
        return False

    # 2. Extract body data
    body = req_payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if user_id is None or new_email is None:
        return False

    # 3. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 4. Update the mock database
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # Simulate atomic update; in real life use transactions
    user_record["email"] = new_email
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate mock database
    database[1] = {"email": "old@example.com"}

    request_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "new@example.com"}
    }

    success = edit_user_email(request_payload)
    print("Update successful:", success)          # Expected: True
    print("Updated email:", database[1]["email"])  # Expected: new@example.com