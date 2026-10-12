import requests
from typing import Optional, Dict

# Global dictionary mapping user IDs to their trusted cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user1": "abc123",
    "user2": "def456",
    # Add more trusted profiles as needed.
}

# Base URL of the remote service providing user profiles.
BASE_URL = "https://example.com/api/users"

def _fetch_profile(u_id: str) -> Dict:
    """
    Internal helper to retrieve the user profile from the remote service.
    Raises requests.exceptions.ConnectionError if the request fails.
    """
    url = f"{BASE_URL}/{u_id}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raises HTTPError for bad status codes.
    return response.json()


def get_user_details(u_id: str, sig_code: str) -> Optional[Dict]:
    """
    Retrieve a user profile from the remote service and validate its cryptographic signature.

    Parameters
    ----------
    u_id : str
        Unique identifier for the user.
    sig_code : str
        Cryptographic signature provided with the profile.

    Returns
    -------
    dict or None
        The user profile if the signature matches a trusted value; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    try:
        profile = _fetch_profile(u_id)
    except requests.exceptions.RequestException as exc:
        # Convert any request-related exception into a ConnectionError.
        raise ConnectionError(f"Failed to fetch profile for user {u_id}") from exc

    # Validate the signature against the trusted list.
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if expected_sig is None:
        # No trusted signature known for this user; reject the profile.
        return None

    if sig_code != expected_sig:
        # Signature mismatch; reject the profile.
        return None

    return profile