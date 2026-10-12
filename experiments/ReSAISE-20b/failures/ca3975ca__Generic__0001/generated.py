import hmac
from typing import Dict

# Simulated database and CSRF token for demonstration purposes
database: Dict[int, dict] = {
    1: {"name": "Alice", "phone": "555-0100"},
    2: {"name": "Bob",   "phone": "555-0200"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Perform a constant‑time comparison to mitigate timing attacks.
    """
    return hmac.compare_digest(val1, val2)


def modify_user_phone(request_data: Dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    request_data : dict
        A dictionary containing:
            - 'headers': dict with a 'X-CSRF-Token' key.
            - 'body':   dict with keys 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was updated successfully,
        False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers")
    if not isinstance(headers, dict):
        return False

    token = headers.get("X-CSRF-Token")
    if not isinstance(token, str):
        return False

    if not _constant_time_compare(token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract body parameters
    body = request_data.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Update database entry
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Basic phone number validation: allow digits, spaces, dashes, parentheses, and plus sign
    if not all(ch.isdigit() or ch in " +()-" for ch in new_phone):
        return False

    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": "secure_csrf_token_12345"},
        "body": {"user_id": 1, "new_phone": "+1 (555) 123-4567"},
    }
    print(modify_user_phone(req))          # Expected: True
    print(database[1]["phone"])            # Updated phone number