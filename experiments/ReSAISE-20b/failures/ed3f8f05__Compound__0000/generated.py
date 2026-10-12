import re
from typing import Dict

# Mock database: user_id -> {'email': str, ...}
database: Dict[str, Dict] = {
    "user123": {"email": "old@example.com", "name": "Alice"},
    "user456": {"email": "bob@example.org",  "name": "Bob"},
}

# Expected CSRF token value for validation
EXPECTED_CSRF_TOKEN: str = "s3cr3t-csrf-token"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def change_user_email(request_data: Dict) -> bool:
    """
    Update the email address of a user.

    Parameters
    ----------
    request_data : dict
        A dictionary representing the HTTP request. Expected keys:
            - 'headers': dict containing request headers
            - 'body': dict containing user data with keys:
                * 'user_id'   : str, the identifier of the user to update
                * 'new_email' : str, the new email address

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.

    Raises
    ------
    ValueError
        If required data is missing or invalid.
    """
    # 1. CSRF protection: verify the token in headers
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract body data and validate presence
    body = request_data.get("body")
    if not isinstance(body, dict):
        raise ValueError("Request body must be a dictionary.")

    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not isinstance(user_id, str):
        raise ValueError("Missing or invalid 'user_id'.")
    if not new_email or not isinstance(new_email, str):
        raise ValueError("Missing or invalid 'new_email'.")

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        raise ValueError("Invalid email format.")

    # 4. Verify user exists in the mock database
    user_record = database.get(user_id)
    if not user_record:
        # User ID does not exist
        return False

    # 5. Update the email address
    user_record["email"] = new_email
    return True