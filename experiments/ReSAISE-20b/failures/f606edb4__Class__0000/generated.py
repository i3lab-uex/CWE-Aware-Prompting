import hmac
from typing import Optional, Dict

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in a real system these would be securely stored)
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "alice":   "1a2b3c4d5e6f7g8h9i0j",
    # ... more entries ...
}

def _fetch_remote_profile(uid: str) -> dict:
    """
    Simulate fetching a user profile from a remote system.
    In production this would perform an HTTP request or similar network call.
    Raises ConnectionError if the remote system is unreachable.
    """
    # For demonstration, we pretend to fetch data and raise ConnectionError
    # for a specific UID to illustrate error handling.
    if uid == "unreachable":
        raise ConnectionError(f"Could not connect to remote system for UID {uid}")
    # Dummy profile data
    return {"uid": uid, "name": f"Name of {uid}", "email": f"{uid}@example.com"}

def retrieve_user_info(uid: str, sig: str) -> Optional[dict]:
    """
    Retrieve a user profile and verify its authenticity.

    Parameters
    ----------
    uid : str
        The unique identifier for the user whose profile needs to be fetched.
    sig : str
        The cryptographic signature that was provided with the profile data.

    Returns
    -------
    dict | None
        The user profile if the signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to connectivity issues.
    """
    # Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # No trusted signature known for this UID – treat as invalid
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        # Signature does not match the trusted one
        return None

    # At this point, signature is considered valid; fetch profile data
    try:
        profile = _fetch_remote_profile(uid)
    except ConnectionError as exc:
        # Propagate connectivity errors
        raise

    return profile