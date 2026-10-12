import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary of trusted signatures for user profiles.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted users here.
}

def _fetch_remote_profile(uid: str) -> Dict:
    """
    Simulates fetching a user profile from a remote service.
    In a real implementation this would perform an HTTP request or similar.

    Raises:
        ConnectionError: If the remote service cannot be reached.
    """
    # Simulated network failure for demonstration purposes.
    if uid == "network_error":
        raise ConnectionError("Unable to connect to the remote service.")
    # Simulated profiles.
    fake_profiles = {
        "alice": {"uid": "alice", "name": "Alice Smith", "email": "alice@example.com"},
        "bob":   {"uid": "bob",   "name": "Bob Jones",  "email": "bob@example.com"},
    }
    return fake_profiles.get(uid, {})

def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict]:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Args:
        uid: Unique identifier of the user.
        sig: Cryptographic signature associated with the profile.

    Returns:
        The user profile dictionary if the signature is valid, otherwise None.

    Raises:
        ConnectionError: If the remote service cannot be reached.
    """
    # Fetch profile from remote service.
    try:
        profile = _fetch_remote_profile(uid)
    except Exception as e:
        # Re‑raise as ConnectionError for consistency.
        raise ConnectionError(f"Failed to fetch profile for uid '{uid}': {e}") from e

    if not profile:
        # No profile found for this uid.
        return None

    # Retrieve the expected signature from trusted store.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # The user is not trusted; reject the profile.
        return None

    # Perform a constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch; do not trust the profile.
        return None

    # Signature verified – return the trusted profile.
    return profile