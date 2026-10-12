import hmac
from typing import Dict

# Simulated database and CSRF token
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

def discard_user(req_info: Dict) -> bool:
    """
    Delete a user account identified by the 'user_id' field in req_info['body'].
    
    Parameters
    ----------
    req_info : dict
        Dictionary representing the HTTP request. It must contain:
            - 'headers': a dictionary of request headers.
            - 'body': a dictionary containing at least the key 'user_id'.
    
    Returns
    -------
    bool
        True if the user was deleted successfully, False otherwise.
    
    Notes
    -----
    - The function performs a constant‑time comparison of the CSRF token to mitigate
      timing attacks (CWE‑693).
    - It validates that the request contains a user_id and that the token matches
      before attempting deletion.
    - If the user does not exist in the database, the function returns False.
    """
    # Validate request structure
    if not isinstance(req_info, dict):
        return False

    headers = req_info.get("headers", {})
    body = req_info.get("body", {})

    # Extract CSRF token from headers (e.g., X-CSRF-Token)
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if not csrf_token:
        return False

    # Constant‑time comparison of CSRF tokens
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract user ID
    user_id = body.get("user_id")
    if not user_id:
        return False

    # Attempt to delete the user
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User not found; treat as failure
            return False
    except Exception:
        # Any unexpected exception leads to a safe failure
        return False