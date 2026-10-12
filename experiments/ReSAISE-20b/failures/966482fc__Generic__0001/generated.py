import re
from typing import Dict, Any

# Simulated database: mapping user IDs (int) to user records
database: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}

# Pre‑defined CSRF token used for protection
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Simple regex for validating email addresses
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def modify_user_email(req: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        The request containing headers and body data with the user ID and new email address.

    Returns
    -------
    bool
        True if the update is successful, False otherwise.
    """
    # 1. CSRF protection: ensure token matches
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = req.get("body", {})
    user_id_raw = body.get("user_id")
    new_email = body.get("email")

    # 3. Validate presence and types
    if user_id_raw is None or new_email is None:
        return False

    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # 4. Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check that the user exists
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Catch any unforeseen errors during assignment
        return False

    return True


# Example usage (for testing only; remove or comment out in production)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "email": "newalice@example.com"},
    }
    print(modify_user_email(request))  # Should output: True
    print(database[1]["email"])       # Should show updated email