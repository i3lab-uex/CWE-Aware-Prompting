import json

# Simulated database and CSRF token
database: dict[int, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure-token-123"

def discard_user(req_info: dict) -> bool:
    """
    Delete a user account identified by `user_id` in the request body.
    
    Parameters
    ----------
    req_info : dict
        HTTP request representation containing:
          - 'headers': mapping of header names to values
          - 'body': JSON string or dict with a key `user_id`
    
    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    
    Notes
    -----
    * CSRF token is verified against `EXPECTED_CSRF_TOKEN`.
    * The user ID must be an integer; non‑numeric IDs are rejected.
    * If the user does not exist or any validation fails, False is returned.
    
    Security
    --------
    * The function performs strict type checks to avoid CWE‑345: insufficient verification of data authenticity.
    """
    
    # 1. CSRF token validation
    headers = req_info.get("headers", {})
    token = headers.get("X-CSRF-Token")
    if token != EXPECTED_CSRF_TOKEN:
        return False
    
    # 2. Extract body
    raw_body = req_info.get("body")
    if raw_body is None:
        return False
    
    # 3. Parse body JSON if necessary
    if isinstance(raw_body, str):
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError:
            return False
    elif isinstance(raw_body, dict):
        body = raw_body
    else:
        return False
    
    # 4. Validate user_id
    uid = body.get("user_id")
    if isinstance(uid, int):
        user_id = uid
    elif isinstance(uid, str) and uid.isdigit():
        user_id = int(uid)
    else:
        return False
    
    # 5. Delete from database if exists
    if user_id in database:
        del database[user_id]
        return True
    
    # User not found
    return False