import json
import hmac
import hashlib
from typing import Any, Dict, Optional

# Global dictionary mapping user IDs to the expected cryptographic signature of their profile.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (signature values are placeholders)
    "user123": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "user456": "5d41402abc4b2a76b9719d911017c592",
    # ... more entries ...
}

# In a real system the secret key would be kept securely (e.g., environment variable, HSM)
SECRET_KEY = b"super_secret_key"

def _fetch_profile_from_service(uid: str) -> Dict[str, Any]:
    """
    Simulate fetching user profile data from an external service.
    In a real implementation this would use `requests.get` or another HTTP client.
    """
    # For demonstration, we just return a deterministic dictionary
    # based on the uid. In practice replace this with an actual HTTP request.
    profiles = {
        "user123": {"uid": "user123", "name": "Alice", "email": "alice@example.com"},
        "user456": {"uid": "user456", "name": "Bob", "email": "bob@example.com"},
    }
    if uid not in profiles:
        raise ConnectionError(f"Profile for UID {uid} could not be retrieved.")
    return profiles[uid]

def _compute_signature(data: bytes) -> str:
    """
    Compute an HMAC-SHA256 signature for the given data using the secret key.
    The result is returned as a hexadecimal string.
    """
    mac = hmac.new(SECRET_KEY, msg=data, digestmod=hashlib.sha256)
    return mac.hexdigest()

def retrieve_user_data(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its signature.

    Args:
        uid: The identifier of the user whose profile is being fetched.
        sig: The cryptographic signature attached to the profile data.

    Returns:
        The user profile dictionary if the signature is valid, otherwise None.

    Raises:
        ConnectionError: If the external service fails to provide the profile data.
    """
    # Step 1: Fetch raw profile data from external service
    try:
        profile = _fetch_profile_from_service(uid)
    except Exception as exc:   # pragma: no cover
        raise ConnectionError(f"Failed to retrieve profile for UID {uid}") from exc

    # Step 2: Compute expected signature of the fetched data
    profile_bytes = json.dumps(profile, sort_keys=True).encode("utf-8")
    expected_sig = _compute_signature(profile_bytes)

    # Step 3: Verify the provided signature against the expected one
    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch: do not trust the data
        return None

    # Step 4: Optional: verify that the provided signature matches the stored trusted one
    stored_sig = TRUSTED_USER_PROFILES.get(uid)
    if stored_sig is None or not hmac.compare_digest(sig, stored_sig):
        # The signature is not recognized as trusted for this UID
        return None

    return profile