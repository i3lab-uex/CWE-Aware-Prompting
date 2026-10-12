import re

# Simulated database and CSRF token
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def update_user_email(request: dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    request : dict
        Expected keys:
            - 'headers': dict containing the CSRF token under 'X-CSRF-Token'
            - 'body': dict containing:
                * 'user_id' (int)
                * 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Notes
    -----
    - The function performs a strict CSRF token check.
    - Email format is validated with a regular expression.
    - The function ensures that the user ID exists before updating.
    """
    try:
        # 1. Verify CSRF token
        headers = request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract body parameters
        body = request.get("body", {})
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        # 3. Basic input validation
        if not isinstance(user_id, int) or not isinstance(new_email, str):
            return False

        # 4. Validate email format
        if not EMAIL_REGEX.match(new_email):
            return False

        # 5. Check that the user exists in the database
        if user_id not in database:
            return False

        # 6. Perform the update
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # In case of any unexpected error, fail safely
        return False