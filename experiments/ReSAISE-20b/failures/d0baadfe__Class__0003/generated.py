import re
import hmac

# Sample context variables (would normally be defined elsewhere)
database = {
    # user_id: {"phone": "1234567890", ...}
    1: {"name": "Alice", "phone": "5551234567"},
    2: {"name": "Bob",   "phone": "5559876543"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a basic international phone number (E.164 format)
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def modify_user_phone(user_request: dict) -> bool:
    """
    Update the phone number for a user in the `database`.

    Parameters
    ----------
    user_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body": {"user_id": <int>, "new_phone": "<phone string>"}
            }

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    try:
        # 1. Verify CSRF token (constant‑time comparison)
        headers = user_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
            return False

        # 2. Extract user ID and new phone number
        body = user_request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not isinstance(user_id, int) or user_id <= 0:
            return False
        if not isinstance(new_phone, str):
            return False

        # 3. Validate phone number format
        if not PHONE_REGEX.match(new_phone):
            return False

        # 4. Update the database
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Perform the update atomically
        user_record["phone"] = new_phone
        return True

    except Exception:
        # In production, log the exception but do not expose details
        return False