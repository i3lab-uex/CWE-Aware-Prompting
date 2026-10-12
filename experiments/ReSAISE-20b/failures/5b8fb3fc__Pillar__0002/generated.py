import requests
import hmac
from typing import Optional, Dict

# Example trusted signatures for known user IDs.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "e3b0c44298fc1c149afbf4c8996fb924",
    "bob":   "a54d88e06612d820bc3be72877c74f257b561b19",
    # ... add more trusted user signatures here ...
}

def _fetch_profile_from_remote(uid: str) -> Dict:
    """
    Internal helper that fetches a user profile from the remote service.
    Raises ConnectionError if the request fails or returns a non-200 status code.
    """
    url = f"https://api.example.com/users/{uid}"
    try:
        resp = requests.get(url, timeout=5)  # 5‑second timeout
    except (requests.ConnectionError,
            requests.Timeout,
            requests.RequestException) as exc:
        raise ConnectionError(f"Unable to reach remote service for user {uid}") from exc

    if resp.status_code != 200:
        raise ConnectionError(f"Remote service returned {resp.status_code} for user {uid}")

    try:
        return resp.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(f"Invalid JSON response for user {uid}") from exc


def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict]:
    """
    Retrieve a user profile from the remote service and validate its signature.

    Parameters
    ----------
    uid : str
        The unique identifier for the user whose profile is being fetched.
    sig : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    dict | None
        The user profile if the signature matches a trusted value; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # Validate signature against trusted value using constant‑time comparison
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig or not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch – do not proceed with profile retrieval
        return None

    # Fetch the profile only after signature validation
    try:
        profile = _fetch_profile_from_remote(uid)
    except ConnectionError as exc:
        # Propagate the connection error
        raise

    return profile