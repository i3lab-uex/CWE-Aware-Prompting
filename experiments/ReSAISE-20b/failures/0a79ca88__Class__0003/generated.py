import hmac
import hashlib
import json
from typing import Optional, Dict

# ------------------------------------------------------------------
# Global data that represents the authoritative mapping of user IDs
# to their expected cryptographic signatures.
# ------------------------------------------------------------------
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "alice":   "deadbeefcafebabe1234",
    # Add more trusted profiles as needed
}

# ------------------------------------------------------------------
# Simulated remote service
# ------------------------------------------------------------------
def _fetch_profile_from_remote(u_id: str) -> Dict:
    """
    Simulates fetching a user profile from a remote service.

    In a real implementation this would perform an HTTP request or
    another form of network communication. For the purposes of this
    exercise we simply return a static dictionary or raise a
    ConnectionError to emulate network failure.
    """
    # Simulated profiles (would normally come from the remote service)
    simulated_profiles = {
        "user123": {"name": "Bob", "age": 30},
        "alice":   {"name": "Alice", "age": 25},
    }

    # Simulate a network failure for unknown users
    if u_id not in simulated_profiles:
        raise ConnectionError(f"Unable to fetch profile for user ID: {u_id}")

    return simulated_profiles[u_id]


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------
def get_user_details(u_id: str, sig_code: str) -> Optional[Dict]:
    """
    Retrieve a user profile from the remote service and verify its
    authenticity using the provided cryptographic signature.

    Parameters:
        u_id (str): Unique identifier of the user.
        sig_code (str): Cryptographic signature provided with the profile.

    Returns:
        dict: The user profile if the signature matches.
        None: If the signature does not match.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # Step 1: Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if expected_sig is None:
        # No trusted signature for this user; reject immediately
        return None

    # Step 2: Verify the provided signature using a constant‑time comparison
    if not hmac.compare_digest(sig_code, expected_sig):
        # Signature mismatch – reject the data
        return None

    # Step 3: Fetch the profile from the remote service
    try:
        profile = _fetch_profile_from_remote(u_id)
    except ConnectionError as exc:
        # Propagate the connection error to indicate fetch failure
        raise

    # Step 4: Return the profile (already verified by signature)
    return profile