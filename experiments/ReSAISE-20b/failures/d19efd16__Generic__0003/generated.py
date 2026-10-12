import json
import hmac
import hashlib
from typing import Optional, Dict

# Simulated external service endpoint (replace with real URL)
PROFILE_SERVICE_URL = "https://api.example.com/profiles/"

# Global dictionary mapping user IDs to their secret keys (used for HMAC verification)
TRUSTED_USER_PROFILES: Dict[str, bytes] = {
    "alice": b"supersecretkey1",
    "bob":   b"supersecretkey2",
    # Add more user IDs and their corresponding secret keys here
}

def _fetch_profile(profile_id: str) -> bytes:
    """
    Retrieve the raw profile data from the external service.
    Raises ConnectionError on any network failure or non‑200 status code.
    """
    import requests  # Imported lazily to avoid unnecessary dependency at module load

    url = f"{PROFILE_SERVICE_URL}{profile_id}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise ConnectionError(f"Failed to fetch profile {profile_id}") from exc

    return response.content  # Return raw bytes for signature verification


def _verify_signature(profile_data: bytes, profile_sig: str, secret_key: bytes) -> bool:
    """
    Verify that the provided signature matches an HMAC‑SHA256 of the profile data.
    Uses a timing‑safe comparison to mitigate timing attacks.
    """
    # Compute HMAC of the data
    computed_sig = hmac.new(secret_key, profile_data, hashlib.sha256).hexdigest()

    # Use compare_digest for constant‑time comparison
    return hmac.compare_digest(computed_sig, profile_sig.lower())


def get_user_info(profile_id: str, profile_sig: str) -> Optional[Dict]:
    """
    Retrieve and return a user profile after verifying its cryptographic signature.

    Parameters
    ----------
    profile_id : str
        Identifier of the target user.
    profile_sig : str
        Hex‑encoded HMAC signature provided alongside the profile data.

    Returns
    -------
    dict | None
        The parsed JSON profile if signature verification succeeds; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # 1. Get the secret key for this user; if unknown, treat as untrusted
    secret_key = TRUSTED_USER_PROFILES.get(profile_id)
    if not secret_key:
        return None

    # 2. Retrieve the raw profile data
    raw_profile = _fetch_profile(profile_id)

    # 3. Verify the signature
    if not _verify_signature(raw_profile, profile_sig, secret_key):
        return None

    # 4. Parse JSON and return
    try:
        profile = json.loads(raw_profile.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Malformed data; treat as untrusted
        return None

    return profile