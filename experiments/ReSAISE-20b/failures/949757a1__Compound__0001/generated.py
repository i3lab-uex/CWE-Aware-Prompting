import re
from typing import Dict

# Sample database and CSRF token for demonstration purposes
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "s3cureT0k3n"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def change_user_contact(transaction_request: Dict) -> bool:
    """
    Update a user's phone number in the database after validating CSRF token
    and input data.

    Args:
        transaction_request (dict): Dictionary containing 'headers' and
            'body'. The body must include:
                - 'user_id': int or str convertible to int
                - 'new_phone': str

    Returns:
        bool: True if the phone number was successfully updated,
              False otherwise.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    # 1. Validate CSRF token
    headers = transaction_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or invalid – reject the request
        return False

    # 2. Extract and validate body fields
    body = transaction_request.get("body", {})
    if not isinstance(body, dict):
        return False

    try:
        user_id_raw = body["user_id"]
        new_phone = body["new_phone"]
    except KeyError:
        # Missing required keys
        return False

    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        # User ID is not an integer
        return False

    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        # Phone number format is invalid
        return False

    # 3. Perform the update if user exists
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Update the phone number
    user_record["phone"] = new_phone
    return True