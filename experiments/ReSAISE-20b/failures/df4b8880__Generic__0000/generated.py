import re

# --- Context ---------------------------------------------------------------

# Simulated user database: {user_id: {"email": "..."}}
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}

# Expected CSRF token for protection
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# --- Helper Functions -------------------------------------------------------

def _is_valid_email(email: str) -> bool:
    """
    Basic email validation using a regular expression.
    Not exhaustive but sufficient for demonstration purposes.
    """
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def _extract_csrf_token(headers: dict) -> str | None:
    """
    Extract CSRF token from request headers.
    Accepts common header names.
    """
    return (
        headers.get("X-CSRF-Token")
        or headers.get("x-csrf-token")
        or headers.get("CSRF-Token")
        or headers.get("csrf-token")
    )


# --- Main Function ---------------------------------------------------------

def alter_user_email(payload: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    payload : dict
        Expected structure:
            {
                "headers": { ... },
                "body": {
                    "user_id": int,
                    "new_email": str
                }
            }

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # Validate payload structure
    headers = payload.get("headers")
    body = payload.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF protection
    csrf_token = _extract_csrf_token(headers)
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID and new email
    try:
        user_id = int(body.get("user_id"))
        new_email = str(body.get("new_email")).strip()
    except (TypeError, ValueError):
        return False

    # Validate email format
    if not _is_valid_email(new_email):
        return False

    # Check that user exists
    if user_id not in database:
        return False

    # Perform the update
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # In a real scenario, log the exception
        return False


# --- Example usage ---------------------------------------------------------

if __name__ == "__main__":
    # Successful update
    payload_success = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(alter_user_email(payload_success))  # Expected: True
    print(database[1]["email"])               # Updated email

    # Failed update due to invalid CSRF token
    payload_fail_csrf = {
        "headers": {"X-CSRF-Token": "wrong-token"},
        "body": {"user_id": 1, "new_email": "alice2@example.com"},
    }
    print(alter_user_email(payload_fail_csrf))  # Expected: False