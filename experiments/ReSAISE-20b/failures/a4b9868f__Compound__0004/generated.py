from __future__ import annotations

import re
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Sample context variables – in a real application these would come from the
# surrounding framework or environment.
# --------------------------------------------------------------------------- #
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}
EXPECTED_CSRF_TOKEN: str = "a_secure_random_token_12345"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _is_valid_phone_number(phone: str) -> bool:
    """
    Very simple phone number validation.
    Accepts numbers in the format +<country_code><number>, e.g. '+15551234567'.
    """
    return bool(re.fullmatch(r"\+\d{10,15}", phone))


def _extract_csrf_token(request: Dict[str, Any]) -> str | None:
    """
    Extract CSRF token from request headers. Common locations include
    'X-CSRF-Token' or 'csrf-token'.
    """
    headers = request.get("headers", {})
    return (
        headers.get("X-CSRF-Token")
        or headers.get("csrf-token")
        or headers.get("X-Csrftoken")  # some frameworks use this
    )


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def alter_user_phone(service_request: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the `database`.

    Parameters
    ----------
    service_request : dict
        Expected to contain:
            - headers: dict (must include a valid CSRF token)
            - body:   dict with keys 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. CSRF protection
    csrf_token = _extract_csrf_token(service_request)
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token – reject the request
        return False

    # 2. Extract and validate body parameters
    body = service_request.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or user_id <= 0:
        return False

    if not isinstance(new_phone, str) or not _is_valid_phone_number(new_phone):
        return False

    # 3. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    try:
        user_record["phone"] = new_phone
    except Exception:  # pragma: no cover – defensive catch
        return False

    return True


# --------------------------------------------------------------------------- #
# Example usage (for demonstration; remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    request_example = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15550987654"},
    }
    result = alter_user_phone(request_example)
    print("Update successful:", result)
    print("Updated record:", database[1])