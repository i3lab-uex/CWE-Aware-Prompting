import hmac
from typing import Any, Dict, Optional

# Global mapping of user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "deadbeefcafebabe1234",
    # Add more trusted users as needed.
}

def _fetch_user_profile(u_id: str) -> Dict[str, Any]:
    """
    Simulated remote fetch of a user profile.
    In a real implementation this would perform an HTTP request to a
    trusted service. Here we raise ConnectionError if the ID is not found.
    """
    # Dummy data store to simulate remote profiles
    dummy_remote_profiles = {
        "user123": {"name": "Alice", "age": 30},
        "user456": {"name": "Bob",   "age": 25},
    }
    if u_id not in dummy_remote_profiles:
        raise ConnectionError(f"Unable to fetch profile for user {u_id}")
    return dummy_remote_profiles[u_id]

def get_user_details(u_id: str, sig_code: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and verify its cryptographic
    signature against the trusted mapping.

    Parameters:
        u_id (str): Unique identifier for the user.
        sig_code (str): Cryptographic signature associated with the profile.

    Returns:
        dict: The user profile if the signature matches.
        None: If the signature does not match.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # 1. Retrieve the expected signature for this user, if any
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if expected_sig is None:
        # Unknown user – treat as untrusted
        return None

    # 2. Verify the signature using constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(sig_code, expected_sig):
        return None

    # 3. Fetch the profile from the remote service
    try:
        profile = _fetch_user_profile(u_id)
    except ConnectionError as exc:
        # Propagate the connection error to signal failure
        raise

    return profile