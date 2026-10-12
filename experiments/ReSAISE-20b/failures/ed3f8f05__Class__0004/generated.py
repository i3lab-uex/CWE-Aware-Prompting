import re
from typing import Dict

# Mock database and CSRF token (would normally be in a secure store)
database: Dict[int, dict] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"}
}
EXPECTED_CSRF_TOKEN = "s3cureT0ken123"

# Regular expression for a simple but reasonable email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def change_user_email(request_data: Dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and input validity.

    Parameters
    ----------
    request_data : dict
        Dictionary representing the HTTP request. Expected keys:
            - 'headers': dict of request headers.
            - 'body': dict containing at least 'user_id' (int) and 'new_email' (str).

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    try:
        headers = request_data.get("headers", {})
        body = request_data.get("body", {})

        # 1. CSRF token verification
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Retrieve and validate user_id
        user_id = body.get("user_id")
        if not isinstance(user_id, int):
            return False

        # 3. Retrieve and validate new_email
        new_email = body.get("new_email")
        if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
            return False

        # 4. Ensure user exists in the mock database
        if user_id not in database:
            return False

        # 5. Perform the update
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # Any unexpected error should result in a failure response.
        return False