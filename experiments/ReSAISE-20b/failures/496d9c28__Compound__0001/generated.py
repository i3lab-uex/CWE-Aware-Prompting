import re

# Simulated database and CSRF token for this example
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure_token_12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$")


def change_user_email(new_request: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and email format.

    Parameters
    ----------
    new_request : dict
        Dictionary containing 'headers' and 'body'.  Expected keys:
            - headers['X-CSRF-Token'] : str
            - body['user_id']        : int or convertible to int
            - body['new_email']      : str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Notes
    -----
    - The function performs a strict CSRF token check.
    - Email format is validated using a simple regex; for production use
      consider more robust validation.
    - The function is intentionally defensive: missing keys, type errors,
      or invalid data all result in a False return.
    """
    try:
        # 1. Validate CSRF token
        headers = new_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate user_id
        body = new_request.get("body", {})
        user_id_raw = body.get("user_id")
        if user_id_raw is None:
            return False
        try:
            user_id = int(user_id_raw)
        except (TypeError, ValueError):
            return False

        # 3. Validate new email format
        new_email = body.get("new_email")
        if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
            return False

        # 4. Check that the user exists in the database
        if user_id not in database:
            return False

        # 5. Perform the update
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # Any unexpected exception should not expose internal details
        return False