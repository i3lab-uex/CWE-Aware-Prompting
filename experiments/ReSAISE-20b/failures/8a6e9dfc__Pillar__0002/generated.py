import re

# Simulated database and CSRF token for the example
database = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@domain.com"}
}
EXPECTED_CSRF_TOKEN = "securetoken123"

# Simple email validation regex (not exhaustive but sufficient for demo)
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]{2,}$")


def edit_user_email(payload: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Args:
        payload: dict containing 'headers' and 'body'.
                 headers must include 'X-CSRF-Token'.
                 body must contain 'user_id' (int) and 'new_email' (str).

    Returns:
        True if the update succeeded, False otherwise.
    """
    try:
        # 1. CSRF token validation
        headers = payload.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate body data
        body = payload.get("body", {})
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        if not isinstance(user_id, int) or not isinstance(new_email, str):
            return False

        # Basic email format check
        if not EMAIL_REGEX.match(new_email):
            return False

        # 3. Perform the update in the simulated database
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Avoiding side effects: update only the email field
        user_record["email"] = new_email
        return True

    except Exception:
        # In case of unexpected errors, fail silently and return False
        return False