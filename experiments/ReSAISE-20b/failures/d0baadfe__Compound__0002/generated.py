import re
from typing import Dict, Any

# Preconfigured CSRF token for validation
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

# Sample user database (user_id -> dict of attributes)
database: Dict[str, Dict[str, Any]] = {
    "user1": {"phone": "+15551234567"},
    "user2": {"phone": "+15559876543"},
}

# Regular expression for a basic E.164 phone number format
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def _validate_csrf_token(request_headers: Dict[str, str]) -> bool:
    """Return True if the CSRF token in headers matches the expected value."""
    # Header names are case‑insensitive; normalize to lowercase
    token = request_headers.get("x-csrf-token") or request_headers.get("X-CSRF-Token")
    return token == EXPECTED_CSRF_TOKEN


def _extract_body(request: Dict[str, Any]) -> Dict[str, str]:
    """Extract the JSON body from the request and validate required fields."""
    if "body" not in request:
        raise ValueError("Missing body in request")
    body = request["body"]
    if not isinstance(body, dict):
        raise ValueError("Body must be a dictionary")
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")
    if not user_id or not isinstance(user_id, str):
        raise ValueError("user_id must be a non‑empty string")
    if not new_phone or not isinstance(new_phone, str):
        raise ValueError("new_phone must be a non‑empty string")
    return {"user_id": user_id, "new_phone": new_phone}


def modify_user_phone(user_request: Dict[str, Any]) -> bool:
    """
    Update the phone number of a user in the database.

    Parameters
    ----------
    user_request : dict
        Dictionary containing request headers and body. The body must contain:
        - 'user_id': str
        - 'new_phone': str (E.164 format)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    if not _validate_csrf_token(headers):
        return False

    # 2. Extract and validate body contents
    try:
        payload = _extract_body(user_request)
    except ValueError:
        return False

    user_id = payload["user_id"]
    new_phone = payload["new_phone"]

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True


# Example usage (for testing only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user1", "new_phone": "+15557654321"}
    }
    print(modify_user_phone(request))  # Should output: True
    print(database["user1"]["phone"])  # Should output the new phone number