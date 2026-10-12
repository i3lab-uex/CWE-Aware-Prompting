import json
import hmac
import hashlib
from typing import Optional, Dict

# Global mapping of user IDs to their trusted signatures (hex strings)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5e884898da28047151d0e56f8dc6292773603d0d6aabbddc",
    "bob":   "7c222fb29255dc7e0d4e3f3d5b9a8c1b",
    # Add more trusted user signatures here
}

# Simulated remote service endpoint (for demonstration purposes)
REMOTE_SERVICE_URL = "https://api.example.com/user_profile"

def _fetch_remote_profile(user_ident: str) -> Dict:
    """
    Simulate a network call to fetch the user profile.
    Raises ConnectionError on failure and returns the JSON payload as a dict.
    """
    # In a real implementation you would use `requests.get` or similar.
    # Here we provide a deterministic stub for demonstration.
    dummy_profiles = {
        "alice": {"name": "Alice", "age": 30},
        "bob":   {"name": "Bob", "age": 25},
    }
    if user_ident not in dummy_profiles:
        raise ConnectionError(f"User {user_ident} not found on remote service.")
    return dummy_profiles[user_ident]

def _verify_signature(user_sig: str, expected_sig: str) -> bool:
    """
    Compare the provided signature with the expected one using constant‑time
    comparison to mitigate timing attacks.
    """
    # Ensure both signatures are bytes for HMAC comparison
    user_sig_bytes = bytes.fromhex(user_sig)
    expected_sig_bytes = bytes.fromhex(expected_sig)
    return hmac.compare_digest(user_sig_bytes, expected_sig_bytes)

def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[Dict]:
    """
    Fetch a user profile from the remote service and verify its authenticity.

    Parameters
    ----------
    user_ident : str
        The unique identifier for the user whose profile is being fetched.
    user_sig : str
        The cryptographic signature associated with the user profile (hex string).

    Returns
    -------
    dict | None
        The user profile dictionary if the signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the remote service.
    """
    # 1. Ensure we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if not expected_sig:
        # Unknown user; cannot trust any signature
        return None

    # 2. Verify the provided signature matches the expected one
    if not _verify_signature(user_sig, expected_sig):
        # Signature mismatch – reject the data
        return None

    # 3. Fetch the profile from the remote service
    try:
        profile = _fetch_remote_profile(user_ident)
    except Exception as exc:  # pragma: no cover
        # Any exception during fetching is treated as a connectivity issue
        raise ConnectionError(f"Failed to fetch profile for {user_ident}") from exc

    # 4. Return the verified profile
    return profile