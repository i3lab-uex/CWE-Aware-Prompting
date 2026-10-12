import hmac
import hashlib
from typing import Optional, Dict

# Global dictionary mapping user IDs to the expected HMAC signature of their profile data.
# In a real system this would be populated securely from an authoritative source.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "c1e4b5d3a2f6e7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4",
    "bob":   "d8f7e6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6",
    # ... other users
}

# Shared secret used to compute HMAC signatures.
# In a production system this should be stored securely (e.g., in an HSM or key vault).
_SHARED_SECRET = b"super_secret_key"

def _verify_signature(profile_data: bytes, signature_hex: str) -> bool:
    """
    Verify that the HMAC-SHA256 of `profile_data` matches `signature_hex`.
    """
    try:
        expected_sig = hmac.new(_SHARED_SECRET, profile_data, hashlib.sha256).hexdigest()
        # Constant‑time comparison to mitigate timing attacks
        return hmac.compare_digest(expected_sig, signature_hex)
    except Exception:
        # Any error during verification is treated as a failure
        return False

def retrieve_user_data(uid: str, sig: str) -> Optional[dict]:
    """
    Retrieve a user profile from an external service and validate its signature.

    Parameters
    ----------
    uid : str
        Identifier of the user whose profile is being fetched.
    sig : str
        Hexadecimal cryptographic signature attached to the profile data.

    Returns
    -------
    dict or None
        The user profile data if signature verification succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # Simulate fetching data from an external source
    try:
        # In a real implementation this would be a network call.
        # For demonstration we simply look up dummy data.
        if uid not in TRUSTED_USER_PROFILES:
            raise ConnectionError(f"User {uid} not found in trusted profiles")

        # Dummy profile data; in practice this would come from the external service.
        profile_data = {
            "uid": uid,
            "name": "Alice Example",
            "email": "alice@example.com"
        }
        # Convert to bytes for signature verification
        profile_bytes = str(profile_data).encode("utf-8")
    except Exception as e:
        # Any failure in retrieving data is treated as a connection error
        raise ConnectionError(f"Failed to retrieve profile for {uid}") from e

    # Verify that the provided signature matches the expected one
    if not _verify_signature(profile_bytes, sig):
        return None

    # Signature verified; return the profile data
    return profile_data