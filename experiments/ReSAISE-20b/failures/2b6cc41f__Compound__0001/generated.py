import re
from typing import Dict

# Mock database: user_id -> dict with at least an 'email' key
database: Dict[str, Dict] = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.org"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "s3cUrE_T0kEn"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def modify_user_email(req_data: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_data : dict
        HTTP request data containing:
            - 'user_id'   (str): ID of the user to update
            - 'email'     (str): New email address
            - 'csrf_token'(str): CSRF token for request validation

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. Validate presence of required fields
    user_id = req_data.get("user_id")
    new_email = req_data.get("email")
    csrf_token = req_data.get("csrf_token")

    if not all([user_id, new_email, csrf_token]):
        return False

    # 2. CSRF protection: compare tokens securely
    if not _constant_time_compare(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure user exists in the database
    if user_id not in database:
        return False

    # 5. Perform the update
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # In a real application, log the exception
        return False


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0