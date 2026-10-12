import json
from typing import Any, Dict, Optional

# Global mapping of user IDs to their trusted cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user_123": "5f2c9e3a1b4d6f8e0c7a9d2b",
    "user_456": "a1b2c3d4e5f6789012345678",
    # Add more trusted user signatures here
}

def _fetch_remote_profile(uid: str) -> Dict[str, Any]:
    """
    Simulates fetching a user profile from a remote service.

    In a real-world scenario this function would perform an HTTP request
    (e.g., using requests.get) to a remote API endpoint. For the purpose of
    this exercise, it simply returns a mock profile.

    Raises:
        ConnectionError: If the remote service cannot be reached.
    """
    # Simulated network failure for demonstration
    if uid == "offline_user":
        raise ConnectionError("Unable to reach the remote service")

    # Mocked user profile data
    return {
        "uid": uid,
        "name": f"User {uid}",
        "email": f"{uid}@example.com",
    }

def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Args:
        uid: The unique identifier for the user.
        sig: The cryptographic signature provided with the profile.

    Returns:
        The user profile dictionary if the signature is valid; otherwise, None.

    Raises:
        ConnectionError: If the remote service cannot be reached.
    """
    # Fetch profile from remote service
    try:
        profile = _fetch_remote_profile(uid)
    except ConnectionError as e:
        # Propagate connection errors
        raise

    # Verify the signature against the trusted mapping
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # User ID not recognized
        return None

    if sig != expected_sig:
        # Signature mismatch; do not trust the profile
        return None

    # All checks passed – return the trusted profile
    return profile

# Example usage (uncomment to test):
# try:
#     prof = retrieve_user_profile("user_123", "5f2c9e3a1b4d6f8e0c7a9d2b")
#     print(prof)
# except ConnectionError as ce:
#     print(f"Connection failed: {ce}")