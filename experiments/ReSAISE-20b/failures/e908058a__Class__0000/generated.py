import json
import urllib.request
import urllib.error
import hmac

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES = {
    # Example entries – replace with real data in production
    "user-123": "a1b2c3d4e5f6g7h8i9j0",
    "user-456": "z9y8x7w6v5u4t3s2r1q0",
}

def _fetch_profile(uuid: str) -> dict:
    """
    Fetch the user profile from a remote endpoint.
    Raises urllib.error.URLError if connectivity fails.
    """
    url = f"https://api.example.com/users/{uuid}/profile"
    with urllib.request.urlopen(url, timeout=10) as resp:
        if resp.status != 200:
            raise urllib.error.URLError(f"HTTP {resp.status}")
        return json.loads(resp.read().decode("utf-8"))

def collect_user_data(uuid: str, sig_hash: str):
    """
    Retrieve a user profile and verify its authenticity.

    Parameters
    ----------
    uuid : str
        Unique identifier of the user.
    sig_hash : str
        Cryptographic signature provided with the profile.

    Returns
    -------
    dict | None
        The user profile if signature is valid; otherwise None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a connectivity issue.
    """
    try:
        profile = _fetch_profile(uuid)
    except urllib.error.URLError as exc:
        # Translate to ConnectionError for caller consistency
        raise ConnectionError(f"Failed to fetch profile for {uuid}") from exc

    # Retrieve the trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if expected_sig is None:
        # Unknown user – treat as invalid signature
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE‑345)
    if hmac.compare_digest(sig_hash, expected_sig):
        return profile
    else:
        # Signature mismatch – do not trust the data
        return None