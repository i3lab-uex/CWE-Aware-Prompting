import hmac
from typing import Any, Dict

# Global mapping of trusted user IDs to their correct signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored.
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted users as needed.
}

def _fetch_remote_profile(u_id: str) -> Dict[str, Any]:
    """
    Simulates fetching a user profile from a remote service.
    In production this would involve network I/O (e.g., HTTP GET).
    Raises ConnectionError if the fetch fails.
    """
    # Placeholder implementation: raise error for unknown IDs
    fake_remote_db = {
        "user123": {"name": "John Doe", "email": "john@example.com"},
        "alice":   {"name": "Alice Smith", "email": "alice@example.com"},
    }
    if u_id not in fake_remote_db:
        raise ConnectionError(f"Could not retrieve profile for user ID '{u_id}'.")
    return fake_remote_db[u_id]

def get_user_details(u_id: str, sig_code: str) -> Dict[str, Any] | None:
    """
    Retrieves a user profile from a remote service and validates its cryptographic
    signature against the trusted list.

    Parameters:
        u_id (str): The unique identifier for the user.
        sig_code (str): The cryptographic signature associated with the profile.

    Returns:
        dict: The user profile if the signature matches.
        None: If the signature does not match.

    Raises:
        ConnectionError: If the remote service cannot be reached or the user is unknown.
    """
    # 1. Fetch profile from remote service
    try:
        profile = _fetch_remote_profile(u_id)
    except ConnectionError as e:
        # Propagate the connection error to caller
        raise

    # 2. Retrieve expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if not expected_sig:
        # Unknown user or missing trusted signature
        return None

    # 3. Perform a timing‑safe comparison of signatures
    if not hmac.compare_digest(sig_code, expected_sig):
        # Signature mismatch – treat as untrusted
        return None

    # 4. All checks passed; return the trusted profile
    return profile