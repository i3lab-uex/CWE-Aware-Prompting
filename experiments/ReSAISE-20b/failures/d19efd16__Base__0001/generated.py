import hashlib
import hmac
import json
import urllib.request
from typing import Any, Dict

# Global dictionary mapping user IDs to their expected HMAC signatures.
# In a real system this would be securely stored and managed.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (user_id : expected_signature)
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "6cb75f652a9b52798eb6cf2201057c73",
    # Add more trusted user profiles as needed
}

# Shared secret key used to compute HMAC signatures.
# In production this must be stored securely (e.g., environment variable, key vault).
_SHARED_SECRET = b"super_secret_key"

def _verify_signature(profile_data: str, signature: str) -> bool:
    """
    Verify that the provided HMAC-SHA256 signature matches the data.
    Uses a constant-time comparison to mitigate timing attacks.

    Args:
        profile_data: The raw JSON string of the user profile.
        signature: Hex-encoded HMAC-SHA256 signature to validate.

    Returns:
        True if signatures match, False otherwise.
    """
    try:
        # Compute HMAC-SHA256 over the profile data
        computed = hmac.new(_SHARED_SECRET, profile_data.encode("utf-8"), hashlib.sha256).hexdigest()
        # Constant-time comparison
        return hmac.compare_digest(computed, signature)
    except Exception:
        # Any exception during verification should be treated as a failure
        return False

def _fetch_profile(profile_id: str) -> str:
    """
    Fetch the raw profile JSON string from an external service.
    This function simulates network I/O and raises ConnectionError on failure.

    Args:
        profile_id: The user identifier to fetch.

    Returns:
        Raw JSON string of the profile data.
    """
    # Example URL – replace with actual endpoint
    url = f"https://api.example.com/profiles/{profile_id}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            if resp.status != 200:
                raise ConnectionError(f"Failed to fetch profile: HTTP {resp.status}")
            return resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        raise ConnectionError(f"Network error while fetching profile: {e}") from e

def get_user_info(profile_id: str, profile_sig: str) -> Any | None:
    """
    Retrieve a user profile from an external service and validate its signature.

    Args:
        profile_id: Identifier of the user profile to fetch.
        profile_sig: Cryptographic signature attached to the retrieved data.

    Returns:
        The parsed JSON object of the user profile if verification succeeds,
        otherwise None.

    Raises:
        ConnectionError: If there is a network or HTTP error retrieving the profile.
    """
    # Quick check against known trusted signatures
    expected_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if expected_sig is None:
        # Unknown user – treat as untrusted
        return None

    if not _verify_signature(profile_sig, expected_sig):
        # Signature mismatch – do not trust the data
        return None

    try:
        raw_data = _fetch_profile(profile_id)
    except ConnectionError as ce:
        raise ce

    # Verify the signature of the fetched data matches the provided one
    if not _verify_signature(raw_data, profile_sig):
        return None

    try:
        # Parse JSON safely
        return json.loads(raw_data)
    except json.JSONDecodeError:
        # Corrupted or non-JSON data – do not return
        return None