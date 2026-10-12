import json
import hmac
import hashlib
from typing import Any, Dict, Optional

# Example trusted signatures for each user (in a real system these would be kept secret)
TRUSTED_USER_PROFILES: Dict[str, bytes] = {
    "alice": b"secret_key_for_alice",
    "bob":   b"secret_key_for_bob",
}

def _fetch_profile(uid: str) -> Dict[str, Any]:
    """
    Simulated external service call that returns a user profile as JSON.
    In a real implementation this would be an HTTP request or database lookup.
    """
    # Dummy data for demonstration purposes
    dummy_profiles = {
        "alice": {"name": "Alice", "age": 30, "email": "alice@example.com"},
        "bob":   {"name": "Bob", "age": 25, "email": "bob@example.com"},
    }
    if uid not in dummy_profiles:
        raise ConnectionError(f"User {uid} not found")
    return dummy_profiles[uid]

def _compute_signature(data: str, key: bytes) -> str:
    """
    Compute HMAC‑SHA256 signature for the given data string using the provided key.
    The result is returned as a hexadecimal string.
    """
    return hmac.new(key, data.encode("utf-8"), hashlib.sha256).hexdigest()

def retrieve_user_data(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile and verify its cryptographic signature.

    Parameters
    ----------
    uid : str
        Identifier of the user whose profile is requested.
    sig : str
        Hexadecimal HMAC‑SHA256 signature attached to the profile data.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # Ensure we have a trusted key for this user
    key = TRUSTED_USER_PROFILES.get(uid)
    if not key:
        # Unknown user – treat as a security failure
        return None

    try:
        profile = _fetch_profile(uid)
    except Exception as exc:
        # Wrap any retrieval error in a ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for {uid}") from exc

    # Convert the profile dict back into a canonical JSON string
    # Sorting keys ensures deterministic ordering for signature calculation.
    profile_json = json.dumps(profile, sort_keys=True)

    # Compute expected signature
    expected_sig = _compute_signature(profile_json, key)

    # Constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(expected_sig, sig):
        return None

    return profile