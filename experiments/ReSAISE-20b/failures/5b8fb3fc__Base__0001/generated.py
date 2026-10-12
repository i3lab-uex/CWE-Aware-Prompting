import hmac
import hashlib
from typing import Optional, Dict

# Global mapping of trusted user IDs to their expected signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in a real system these would be securely stored).
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted profiles here.
}

def _fetch_profile_from_remote(uid: str) -> Dict:
    """
    Simulates fetching a user profile from a remote service.
    In a real implementation this would perform an HTTP request or similar.
    Raises ConnectionError if the remote service is unreachable.
    """
    # For demonstration purposes, we'll pretend that fetching always succeeds
    # for known UIDs and fails otherwise.
    if uid not in TRUSTED_USER_PROFILES:
        raise ConnectionError(f"Unable to fetch profile for UID '{uid}'.")
    # Simulated profile data.
    return {"uid": uid, "name": f"User {uid}", "email": f"{uid}@example.com"}

def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict]:
    """
    Retrieve a user profile from a remote service and validate its cryptographic signature.

    Parameters:
        uid (str): The unique identifier of the user.
        sig (str): The cryptographic signature associated with the fetched profile.

    Returns:
        dict: The user profile if the signature is valid.
        None: If the signature does not match the expected value.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # Step 1: Fetch the profile from the remote service
    try:
        profile = _fetch_profile_from_remote(uid)
    except ConnectionError as e:
        # Propagate the connection error to the caller
        raise

    # Step 2: Retrieve the expected signature for this UID
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # No trusted signature known for this UID; treat as untrusted
        return None

    # Step 3: Perform a constant‑time comparison of the signatures to mitigate timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch – the profile is considered untrusted
        return None

    # Signature matches; return the trusted profile
    return profile