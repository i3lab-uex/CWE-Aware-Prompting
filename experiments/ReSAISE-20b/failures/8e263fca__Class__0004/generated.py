import hmac
import hashlib
import random
from typing import Optional, Dict

# Mock database of trusted profiles (user_id -> signature)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "6cb75f652a9b52798eb6cf2201057c73",
    "carol": "e99a18c428cb38d5f260853678922e03",
}

# Mock remote service that returns a user profile
def _remote_fetch_profile(user_ident: str) -> Dict[str, str]:
    """
    Simulate a remote service that returns user profile data.
    Raises ConnectionError on simulated network failure.
    """
    # Simulate 10% chance of network failure
    if random.random() < 0.1:
        raise ConnectionError(f"Unable to connect to remote service for user {user_ident}")

    # Simulated profiles
    profiles = {
        "alice": {"name": "Alice Smith", "email": "alice@example.com"},
        "bob":   {"name": "Bob Jones",  "email": "bob@example.com"},
        "carol": {"name": "Carol Lee",  "email": "carol@example.com"},
    }
    return profiles.get(user_ident, {})

def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[Dict[str, str]]:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Args:
        user_ident: Unique identifier for the user.
        user_sig:   Cryptographic signature provided with the profile.

    Returns:
        The user profile dictionary if the signature matches; otherwise None.

    Raises:
        ConnectionError: If the remote service cannot be reached.
    """
    # Retrieve expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if not expected_sig:
        # No trusted signature known; reject immediately
        return None

    # Perform constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(user_sig, expected_sig):
        # Signature mismatch – data is untrusted
        return None

    # Fetch the profile from the remote service
    profile = _remote_fetch_profile(user_ident)

    if not profile:
        # Profile does not exist; treat as untrusted
        return None

    return profile