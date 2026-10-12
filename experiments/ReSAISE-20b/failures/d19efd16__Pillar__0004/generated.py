import base64
import hmac
import hashlib
import json
from typing import Optional

# Example trusted signatures (user_id -> base64‑encoded HMAC-SHA256)
TRUSTED_USER_PROFILES = {
    "user123": "u5w3bV9yZ+8YJ4eOZQz6cP0lRk7hS9xN5q2YVj3Zf8=",
    # add more trusted users here
}

# Simulated external service endpoint (for demonstration purposes)
EXTERNAL_SERVICE_URL = "https://api.example.com/user_profile"

def _fetch_user_profile(profile_id: str) -> str:
    """
    Simulate fetching the raw profile data from an external service.
    In a real implementation this would perform an HTTP GET request.
    """
    # Dummy data for illustration; replace with actual network call if needed
    dummy_profiles = {
        "user123": json.dumps({"id": "user123", "name": "Alice", "email": "alice@example.com"}),
        # add more dummy profiles as needed
    }
    if profile_id not in dummy_profiles:
        raise ConnectionError(f"Profile {profile_id} could not be retrieved.")
    return dummy_profiles[profile_id]

def get_user_info(profile_id: str, profile_sig: str) -> Optional[dict]:
    """
    Retrieve a user profile and verify its signature.

    Args:
        profile_id: Identifier of the target user.
        profile_sig: Base64‑encoded cryptographic signature attached to the data.

    Returns:
        The parsed JSON profile if the signature is valid; otherwise None.

    Raises:
        ConnectionError: If fetching the profile from the external service fails.
    """
    # 1. Retrieve raw profile data
    try:
        raw_profile = _fetch_user_profile(profile_id)
    except Exception as exc:          # pragma: no cover
        raise ConnectionError(
            f"Failed to retrieve profile for {profile_id}"
        ) from exc

    # 2. Obtain the expected signature for this user
    trusted_sig_b64 = TRUSTED_USER_PROFILES.get(profile_id)
    if not trusted_sig_b64:
        # No trusted signature found – treat as untrusted
        return None

    # 3. Verify the provided signature matches the trusted one
    try:
        # Decode both signatures from base64
        provided_sig = base64.b64decode(profile_sig)
        expected_sig = base64.b64decode(trusted_sig_b64)
    except (base64.binascii.Error, ValueError):  # pragma: no cover
        return None

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(provided_sig, expected_sig):
        return None

    # 4. Parse JSON profile
    try:
        profile_data = json.loads(raw_profile)
    except json.JSONDecodeError:  # pragma: no cover
        return None

    return profile_data