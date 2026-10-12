import re
import hmac

# Simulated database and expected CSRF token
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"}
}
EXPECTED_CSRF_TOKEN = "s3cr3t-t0k3n"

# Regular expression for a simple international phone number format
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def update_user_phone(request: dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input data.

    Parameters
    ----------
    request : dict
        The request payload. Expected keys:
            - headers: dict containing 'X-CSRF-Token'
            - body: dict containing 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    try:
        # 1. Verify CSRF token using constant‑time comparison
        headers = request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
            return False

        # 2. Extract and validate request body
        body = request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not isinstance(user_id, int) or user_id <= 0:
            return False
        if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
            return False

        # 3. Check that the user exists
        user_record = database.get(user_id)
        if not user_record:
            return False

        # 4. Update the phone number
        user_record["phone"] = new_phone
        return True

    except Exception:
        # Any unexpected error should result in a failure, not an exception leak
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": "s3cr3t-t0k3n"},
        "body": {"user_id": 1, "new_phone": "+15551234567"}
    }
    print(update_user_phone(req))  # Expected: True
    print(database[1]["phone"])   # Updated phone number