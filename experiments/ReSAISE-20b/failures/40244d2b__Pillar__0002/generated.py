import json
import hmac
import hashlib
from typing import Any, Dict, Optional

# Global dictionary mapping user IDs to their expected cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",  # example MD5 hash
    "user456": "e99a18c428cb38d5f260853678922e03",
    # Add more trusted signatures as needed
}

def _fetch_remote_profile(identifier: str) -> Dict[str, Any]:
    """
    Simulate fetching a user profile from a remote system.
    In a real implementation this would involve network I/O (e.g., HTTP request).
    For demonstration purposes, we return a static payload or raise ConnectionError.
    """
    # Simulated remote profiles (normally retrieved over the network)
    simulated_remote_profiles = {
        "user123": {"name": "Alice", "email": "alice@example.com"},
        "user456": {"name": "Bob", "email": "bob@example.com"},
    }

    if identifier not in simulated_remote_profiles:
        # Simulate a connectivity or lookup failure
        raise ConnectionError(f"Unable to fetch profile for identifier: {identifier}")

    return simulated_remote_profiles[identifier]


def _verify_signature(profile_data: Dict[str, Any], provided_sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected one
    for the given user profile. We use HMAC with SHA256 over the JSON-encoded
    profile data and a secret key derived from the identifier.

    For demonstration, we simply compare against the stored signature.
    """
    # In a real scenario you would use a secure key and algorithm.
    # Here we perform a simple deterministic check against TRUSTED_USER_PROFILES.
    expected_sig = TRUSTED_USER_PROFILES.get(profile_data.get("identifier"))
    if not expected_sig:
        return False
    # Use constant-time comparison to avoid timing attacks
    return hmac.compare_digest(provided_sig, expected_sig)


def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile and verify its cryptographic signature.

    Parameters
    ----------
    identifier : str
        The unique user identifier.
    crypt_sig : str
        Cryptographic signature provided with the profile data.

    Returns
    -------
    dict or None
        The user profile if signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to connectivity issues.
    """
    # Fetch the remote profile; may raise ConnectionError
    try:
        profile = _fetch_remote_profile(identifier)
    except ConnectionError as e:
        # Re-raise to signal connectivity failure
        raise

    # Attach identifier for verification (simulating the payload)
    profile_with_id = {"identifier": identifier, **profile}

    # Verify the signature
    if _verify_signature(profile_with_id, crypt_sig):
        return profile
    return None