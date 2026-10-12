import re
from typing import Dict

# Mock database and CSRF token (would normally be defined elsewhere)
database: Dict[int, dict] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def change_user_email(request_data: Dict) -> bool:
    """
    Update a user's email address.

    Parameters
    ----------
    request_data : dict
        A dictionary representing the HTTP request. Expected keys:
            - "headers": a dict of header names to values
            - "body": a dict containing:
                * "user_id" : int or str convertible to int
                * "new_email": str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Raises
    ------
    ValueError
        If CSRF token is missing or invalid, if required fields are missing,
        or if the email format is invalid.
    """
    # 1. CSRF protection
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        raise ValueError("Invalid or missing CSRF token")

    # 2. Extract body data
    body = request_data.get("body", {})
    if not isinstance(body, dict):
        raise ValueError("Request body must be a dictionary")

    user_id_raw = body.get("user_id")
    new_email = body.get("new_email")

    if user_id_raw is None or new_email is None:
        raise ValueError("Missing 'user_id' or 'new_email' in request body")

    # 3. Validate and convert user ID
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        raise ValueError("Invalid 'user_id' format")

    # 4. Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        raise ValueError("Invalid email format")

    # 5. Update database
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Optional: check if email is already in use by another user
    for uid, record in database.items():
        if uid != user_id and record.get("email") == new_email:
            # Email already taken
            return False

    user_record["email"] = new_email
    return True


# Example usage (would normally be part of a test or request handler)
if __name__ == "__main__":
    # Successful update
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    print(change_user_email(req))  # True

    # Failure due to duplicate email
    req_dup = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 2, "new_email": "alice.new@example.com"},
    }
    print(change_user_email(req_dup))  # False