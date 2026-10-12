import re
from typing import Dict

# Simulated environment variables / constants
EXPECTED_CSRF_TOKEN: str = "a1b2c3d4e5f6g7h8i9j0"
# Example simulated database
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}


def _is_valid_email(email: str) -> bool:
    """
    Very simple email validation using a regex.
    This is not exhaustive but protects against obvious malformed input.
    """
    email_regex = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )
    return bool(email_regex.match(email))


def edit_user_email(payload: Dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    payload : dict
        The incoming request object containing:
            - headers: a mapping that must contain 'X-CSRF-Token'
            - body: a mapping with keys 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Notes
    -----
    - The function performs a strict CSRF token check to guard against
      CWE‑345: insufficient verification of data authenticity.
    - The email address is validated with a regex to prevent obvious
      injection or malformed data.
    """
    # 1. Verify CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body payload
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 3. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 4. Ensure user exists in database
    if user_id not in database:
        return False

    # 5. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        return False

    return True


# Example usage (this part is optional and can be removed in production)
if __name__ == "__main__":
    test_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(edit_user_email(test_payload))  # Expected: True
    print(database[1]["email"])           # Expected: alice.new@example.com