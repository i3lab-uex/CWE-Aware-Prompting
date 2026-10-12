import requests
from typing import Optional, Dict
import hmac

# Global dictionary mapping user IDs to their expected signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored
    "user-123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user-456": "e99a18c428cb38d5f260853678922e03",
}

def _fetch_profile(uuid: str) -> Dict:
    """
    Internal helper that retrieves the user profile from a remote service.
    Raises requests.exceptions.RequestException on connectivity issues.
    """
    url = f"https://example.com/api/user/{uuid}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

def collect_user_data(uuid: str, sig_hash: str) -> Optional[Dict]:
    """
    Fetches a user profile from a remote system and verifies its authenticity
    using the provided cryptographic signature.

    Args:
        uuid: Unique identifier for the user.
        sig_hash: Cryptographic signature accompanying the profile data.

    Returns:
        The profile data as a dictionary if the signature is valid;
        otherwise, None.

    Raises:
        ConnectionError: If there was a connectivity issue fetching the profile.
    """
    try:
        profile = _fetch_profile(uuid)
    except requests.exceptions.RequestException as exc:
        # Wrap any network-related exception in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {uuid}") from exc

    # Verify that the signature matches the trusted one
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if expected_sig is None:
        # No trusted signature known for this user
        return None

    if not hmac.compare_digest(sig_hash, expected_sig):
        # Signature mismatch – data is considered untrusted
        return None

    return profile