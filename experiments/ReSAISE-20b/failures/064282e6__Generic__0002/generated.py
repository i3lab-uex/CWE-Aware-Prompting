import hmac
import hashlib
from typing import Any, Dict, Optional

# Global dictionary containing trusted signatures for each user profile.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in practice these would be real cryptographic signatures)
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "6cb75f652a9b52798eb6cf2201057c73",
}

# Simulated external service endpoint (for demonstration purposes only)
EXTERNAL_SERVICE_URL = "https://api.example.com/user_profile"


def _fetch_external_profile(uid: str) -> Dict[str, Any]:
    """
    Simulate a request to an external service that returns user profile data.
    In a real implementation, this would use `requests.get` or similar.
    """
    # For demonstration, raise an error if the user does not exist in our mock data
    mock_profiles = {
        "user123": {"uid": "user123", "name": "John Doe", "email": "john@example.com"},
        "alice":   {"uid": "alice",   "name": "Alice Smith", "email": "alice@example.com"},
    }
    if uid not in mock_profiles:
        raise ConnectionError(f"Failed to retrieve profile for UID: {uid}")
    return mock_profiles[uid]


def _verify_signature(provided_sig: str, expected_sig: str) -> bool:
    """
    Compare two signatures in constant time to mitigate timing attacks.
    Assumes both signatures are hexadecimal strings.
    """
    # Convert hex strings to bytes for compare_digest
    try:
        provided_bytes = bytes.fromhex(provided_sig)
        expected_bytes = bytes.fromhex(expected_sig)
    except ValueError:
        # If conversion fails, signatures are invalid
        return False

    return hmac.compare_digest(provided_bytes, expected_bytes)


def retrieve_user_data(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and validate its signature.

    Parameters
    ----------
    uid : str
        Identifier for the targeted user whose profile is being fetched.
    sig : str
        Cryptographic signature attached to the profile data (hex string).

    Returns
    -------
    dict or None
        The user profile data if the signature verification succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # Step 1: Retrieve expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # No trusted signature available for this UID
        return None

    # Step 2: Verify the provided signature against the trusted one
    if not _verify_signature(sig, expected_sig):
        return None

    # Step 3: Fetch the profile data from the external service
    try:
        profile = _fetch_external_profile(uid)
    except Exception as exc:
        # Wrap any exception as a ConnectionError
        raise ConnectionError(f"Unable to retrieve profile for UID {uid}") from exc

    return profile