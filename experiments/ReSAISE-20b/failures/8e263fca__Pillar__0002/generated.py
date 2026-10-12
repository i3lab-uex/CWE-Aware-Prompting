import hmac
import hashlib
import json
from typing import Optional, Dict

# Global dictionary mapping user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "6f1ed002ab5595859014ebf0951522d9",
    # Add more trusted users here
}

def _fetch_remote_profile(user_ident: str) -> Dict:
    """
    Simulates fetching a user profile from a remote service.
    In a real implementation, this would perform an HTTP request or similar.
    Raises ConnectionError if the remote service is unreachable.
    """
    # Simulated profiles
    simulated_profiles = {
        "alice": {"name": "Alice", "email": "alice@example.com"},
        "bob":   {"name": "Bob",   "email": "bob@example.com"},
    }
    if user_ident not in simulated_profiles:
        # Simulate a network failure for unknown users
        raise ConnectionError(f"Unable to fetch profile for user '{user_ident}'.")
    return simulated_profiles[user_ident]

def _verify_signature(provided_sig: str, expected_sig: str) -> bool:
    """
    Verify the cryptographic signature using constant‑time comparison.
    Uses SHA256 hex digest for demonstration purposes; adjust as needed.
    """
    # Ensure both signatures are in the same format
    provided_sig = provided_sig.lower()
    expected_sig = expected_sig.lower()

    # Constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(provided_sig, expected_sig)

def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[Dict]:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Args:
        user_ident: Unique identifier for the user.
        user_sig:   Cryptographic signature associated with the profile.

    Returns:
        The user profile dictionary if the signature is valid; otherwise None.

    Raises:
        ConnectionError: If the remote service cannot be reached or
                          the user profile is unavailable.
    """
    # Step 1: Retrieve the expected signature from trusted profiles
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if expected_sig is None:
        # Unknown user; treat as untrusted
        return None

    # Step 2: Verify the provided signature
    if not _verify_signature(user_sig, expected_sig):
        # Signature mismatch; do not trust the profile
        return None

    # Step 3: Fetch the profile from the remote service
    try:
        profile = _fetch_remote_profile(user_ident)
    except ConnectionError as exc:
        # Propagate the connection error
        raise

    return profile