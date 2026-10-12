import re

# Global context variables (would normally be provided by the framework)
database: dict = {}                     # Simulated user database
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

# Regular expression for a simple phone number validation (digits, optional + and spaces)
PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")


def change_user_phone(payload: dict) -> bool:
    """
    Update the phone number for a user in the simulated database.

    Parameters
    ----------
    payload : dict
        Dictionary containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with keys:
                * user_id : str
                * phone   : str

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    * CSRF token is validated against EXPECTED_CSRF_TOKEN.
    * The function checks that the payload contains the required fields
      and that `phone` matches a simple numeric pattern.
    * The function is intentionally defensive to avoid CWE-345
      (insufficient verification of data authenticity).
    """
    # 1. Validate CSRF token
    try:
        headers = payload["headers"]
        csrf_token = headers.get("X-CSRF-Token")
    except (KeyError, AttributeError):
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    try:
        body = payload["body"]
        user_id = body["user_id"]
        new_phone = body["phone"]
    except (KeyError, TypeError):
        return False

    # 3. Basic type checks
    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    # 4. Phone number format validation
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Perform the update in a controlled manner
    if user_id not in database:
        return False

    # Simulate atomic update (in real DB, use transactions)
    database[user_id]["phone"] = new_phone
    return True


# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    # Setup a dummy user
    database["user123"] = {"name": "Alice", "phone": "+1112223333"}

    # Valid payload
    payload_valid = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "phone": "+4445556666"}
    }
    assert change_user_phone(payload_valid) is True
    assert database["user123"]["phone"] == "+4445556666"

    # Invalid CSRF
    payload_bad_csrf = {
        "headers": {"X-CSRF-Token": "bad_token"},
        "body": {"user_id": "user123", "phone": "+7778889999"}
    }
    assert change_user_phone(payload_bad_csrf) is False