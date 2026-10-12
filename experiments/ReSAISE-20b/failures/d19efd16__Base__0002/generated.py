import json
import hmac
import hashlib
from typing import Any, Dict, Optional

# Simulated external service endpoint (replace with the real URL)
EXTERNAL_PROFILE_ENDPOINT = "https://api.example.com/user/profile"

# Example trusted signatures for user profiles.
# In a real system these would be securely stored and managed.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",  # Example MD5 hex digest
    "alice":   "e99a18c428cb38d5f260853678922e03",
    # ... other user IDs ...
}

def get_user_info(profile_id: str, profile_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its signature.

    Args:
        profile_id: Identifier of the target user.
        profile_sig: Cryptographic signature attached to the profile data.

    Returns:
        The user profile data as a dictionary if the signature is valid,
        otherwise None.

    Raises:
        ConnectionError: If the profile cannot be retrieved from the external service.
    """
    # 1. Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if not expected_sig:
        # No trusted signature known for this user
        return None

    # 2. Compare the provided signature with the expected one in a constant‑time manner
    if not hmac.compare_digest(profile_sig.lower(), expected_sig.lower()):
        # Signature mismatch – do not trust the data
        return None

    # 3. Fetch profile data from the external service
    try:
        response = requests.get(
            f"{EXTERNAL_PROFILE_ENDPOINT}/{profile_id}",
            timeout=5.0,  # seconds
        )
    except Exception as exc:
        raise ConnectionError(f"Failed to connect to external service: {exc}") from exc

    if response.status_code != 200:
        raise ConnectionError(
            f"External service returned status {response.status_code}"
        )

    # 4. Parse JSON payload
    try:
        profile_data = response.json()
    except ValueError as exc:  # includes json.JSONDecodeError
        raise ConnectionError(f"Invalid JSON response: {exc}") from exc

    # 5. Optional sanity check: ensure profile data contains expected fields
    if not isinstance(profile_data, dict) or "id" not in profile_data:
        return None

    # 6. Return the verified profile data
    return profile_data