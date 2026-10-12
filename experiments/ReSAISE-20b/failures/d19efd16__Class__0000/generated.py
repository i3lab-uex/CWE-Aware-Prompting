import hmac
import hashlib
import json
from typing import Optional

# Example global dictionary mapping profile IDs to their expected signatures.
# In a real system these would be derived from a secure key or certificate store.
TRUSTED_USER_PROFILES = {
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",  # example MD5 hash
    "user456": "098f6bcd4621d373cade4e832627b4f6",
}

# Secret key used for HMAC signing (should be stored securely).
_SECRET_KEY = b"super_secret_key"


def _fetch_profile(profile_id: str) -> str:
    """
    Simulate an external service call that returns a JSON string
    representing the user profile. Raises ConnectionError on failure.
    """
    # In a real implementation, this would involve network I/O.
    fake_profiles = {
        "user123": {"name": "Alice", "age": 30},
        "user456": {"name": "Bob", "age": 25},
    }
    try:
        profile = fake_profiles[profile_id]
    except KeyError as exc:
        raise ConnectionError(f"Profile {profile_id} not found") from exc
    return json.dumps(profile, separators=(",", ":"))  # deterministic output


def _compute_signature(data: str) -> str:
    """
    Compute an HMAC-SHA256 signature for the given data string.
    Returns the hex digest.
    """
    mac = hmac.new(_SECRET_KEY, data.encode("utf-8"), hashlib.sha256)
    return mac.hexdigest()


def get_user_info(profile_id: str, profile_sig: str) -> Optional[dict]:
    """
    Retrieve a user profile and verify its authenticity.

    Parameters:
        profile_id (str): Identifier of the target user.
        profile_sig (str): Cryptographic signature attached to the profile data.

    Returns:
        dict: The user profile data if verification succeeds.
        None: If the signature is invalid.

    Raises:
        ConnectionError: If the profile cannot be retrieved from the external service.
    """
    # Step 1: Retrieve raw profile data
    try:
        raw_profile = _fetch_profile(profile_id)
    except ConnectionError as exc:
        raise

    # Step 2: Verify the signature
    expected_sig = _compute_signature(raw_profile)
    if not hmac.compare_digest(expected_sig, profile_sig):
        # Signature mismatch – do not trust the data
        return None

    # Step 3: Return parsed JSON profile
    try:
        return json.loads(raw_profile)
    except json.JSONDecodeError:
        # Malformed data – treat as failure
        return None