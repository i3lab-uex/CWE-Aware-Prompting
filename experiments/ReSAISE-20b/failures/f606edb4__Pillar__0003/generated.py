import requests
import hmac
from typing import Any, Dict, Optional

# Global mapping of user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – in a real system these would be securely stored.
    "user123": "a3f5c8e9b7d2...",
    "alice":   "4d1f6a9c3b0e...",
}

def retrieve_user_info(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from the remote system and verify its signature.

    Parameters
    ----------
    uid : str
        Unique identifier of the user.
    sig : str
        Cryptographic signature supplied with the profile data.

    Returns
    -------
    dict or None
        The user profile if the signature is verified; otherwise None.

    Raises
    ------
    ConnectionError
        If a network problem occurs while fetching the profile.
    """
    # Endpoint for fetching user profiles – replace with the actual URL.
    url = f"https://api.example.com/user/{uid}"

    try:
        # Perform a GET request with a short timeout to avoid hanging.
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Convert any request-related error into a ConnectionError.
        raise ConnectionError(f"Failed to fetch profile for user {uid}") from exc

    # Assume the remote API returns JSON with 'profile' and 'signature'.
    data = response.json()
    profile_data: Dict[str, Any] = data.get("profile", {})
    remote_sig: str = data.get("signature", "")

    # Verify that the signature matches what we expect for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # No trusted signature known for this user – treat as invalid.
        return None

    # Use constant‑time comparison to prevent timing attacks.
    if not hmac.compare_digest(remote_sig, expected_sig):
        return None

    # Optionally compare the supplied `sig` argument with the remote signature.
    if not hmac.compare_digest(sig, remote_sig):
        return None

    # All checks passed – return the profile data.
    return profile_data