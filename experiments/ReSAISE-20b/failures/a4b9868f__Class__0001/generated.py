import re
import hmac

# Sample database and CSRF token for the demonstration
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"}
}
EXPECTED_CSRF_TOKEN = "securetoken123"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+\d{7,15}$")

def alter_user_phone(service_request: dict) -> bool:
    """
    Update a user's phone number in the database after validating CSRF token
    and input data.

    Parameters
    ----------
    service_request : dict
        Expected to contain:
            headers : dict
                Must include 'X-CSRF-Token'
            body   : dict
                Must contain 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    try:
        # 1. Validate CSRF token
        headers = service_request.get("headers", {})
        incoming_token = headers.get("X-CSRF-Token")
        if not incoming_token:
            return False
        # Constant‑time comparison to mitigate timing attacks
        if not hmac.compare_digest(incoming_token, EXPECTED_CSRF_TOKEN):
            return False

        # 2. Extract and validate body payload
        body = service_request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # 3. Validate phone number format
        if not PHONE_REGEX.match(new_phone):
            return False

        # 4. Update database if user exists
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Optional: Ensure the new phone is different from current
        if user_record.get("phone") == new_phone:
            return True  # No change needed, but operation considered successful

        user_record["phone"] = new_phone
        return True

    except Exception:
        # Log the exception in real applications; swallow here for safety
        return False