import re
from typing import Dict

# Mock database: mapping user_id (int) to a dict of user attributes
database: Dict[int, Dict[str, str]] = {
    1: {"email": "alice@example.com", "name": "Alice"},
    2: {"email": "bob@example.com",   "name": "Bob"},
}

# Expected CSRF token used for validation
EXPECTED_CSRF_TOKEN = "s3cr3t_csrf_t0k3n"

# Regular expression for a basic but reasonably strict email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def modify_user_email(req_data: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_data : dict
        A dictionary representing an HTTP request. It must contain:
            - ``headers`` (dict): HTTP headers, including the CSRF token.
            - ``body``   (dict): Payload with keys ``user_id`` and ``new_email``.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    * CSRF protection is performed by comparing the token in the request headers
      with ``EXPECTED_CSRF_TOKEN`` using a constant‑time comparison to avoid timing attacks.
    * The function validates that the new email has a syntactically correct format
      before applying the change.
    * If the user ID does not exist in ``database`` or any validation fails,
      the function returns False without modifying the database.
    """
    # ------------------------------------------------------------------
    # 1. CSRF token validation
    # ------------------------------------------------------------------
    headers = req_data.get("headers", {})
    received_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if not received_token:
        return False

    # Constant‑time comparison to mitigate timing attacks
    if not _constant_time_compare(received_token, EXPECTED_CSRF_TOKEN):
        return False

    # ------------------------------------------------------------------
    # 2. Extract and validate request body
    # ------------------------------------------------------------------
    body = req_data.get("body", {})
    user_id_raw = body.get("user_id")
    new_email = body.get("new_email")

    # Ensure user ID is an integer
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # Validate new email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # ------------------------------------------------------------------
    # 3. Update the mock database
    # ------------------------------------------------------------------
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["email"] = new_email.strip()
    return True


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to avoid timing attacks.
    Returns True if they are equal, False otherwise.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0