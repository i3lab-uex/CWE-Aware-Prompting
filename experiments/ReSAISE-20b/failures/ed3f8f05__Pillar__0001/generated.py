import re

# Mock database and CSRF token for demonstration purposes
database = {
    # user_id: {"email": "...", "name": "..."}
}
EXPECTED_CSRF_TOKEN = "expected_csrf_token_value"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")

def change_user_email(request_data: dict) -> bool:
    """
    Update the email address of a user in a mock database.

    Parameters
    ----------
    request_data : dict
        Dictionary containing the HTTP request data. Expected keys:
            - 'headers': dict, must contain 'X-CSRF-Token'
            - 'body': dict, must contain:
                * 'user_id' (int or str)
                * 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    try:
        headers = request_data.get("headers", {})
        body = request_data.get("body", {})

        # 1. CSRF protection check
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
            # CSRF validation failed
            return False

        # 2. Extract user ID and new email from body
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        if user_id is None or new_email is None:
            # Missing required fields
            return False

        # 3. Validate email format
        if not EMAIL_REGEX.match(new_email):
            return False

        # 4. Check that the user exists in the database
        if user_id not in database:
            return False

        # 5. Perform the update
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # Log exception in real application; swallow error for this mock
        return False