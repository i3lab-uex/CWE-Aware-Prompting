import json
import secrets
import urllib.request
from typing import Optional, Dict

# Global mapping of user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "f5a1c8d9e3b7c4...",
    "bob":   "9c2b1a3f8d0e6b7...",
    # Add more trusted users here
}

def _fetch_remote_profile(uid: str) -> Dict:
    """
    Simulate fetching a user profile from a remote service.

    In a real implementation this would make an HTTP request to a
    trusted API endpoint. For demonstration purposes we use a static
    mapping, but any failure during the request should raise
    ConnectionError.
    """
    # Example URL (replace with actual endpoint)
    url = f"https://api.example.com/users/{uid}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            if resp.status != 200:
                raise ConnectionError(f"Unexpected status code: {resp.status}")
            data = resp.read()
            return json.loads(data)
    except urllib.error.URLError as exc:
        # Convert all URL errors to a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for {uid}") from exc

def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict]:
    """
    Retrieve a user profile from the remote service and validate its
    signature against the trusted mapping.

    Parameters:
        uid: Unique user identifier.
        sig: Cryptographic signature associated with the profile.

    Returns:
        The user profile dictionary if the signature matches the
        trusted value; otherwise None.

    Raises:
        ConnectionError: If the profile cannot be fetched from the
                         remote service.
    """
    # Fetch the profile; propagate any ConnectionError
    profile = _fetch_remote_profile(uid)

    # Retrieve the expected signature for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)

    # If we don't have a trusted signature, reject the profile.
    if expected_sig is None:
        return None

    # Use constant‑time comparison to avoid timing attacks.
    if not secrets.compare_digest(sig, expected_sig):
        return None

    # All checks passed – return the profile.
    return profile