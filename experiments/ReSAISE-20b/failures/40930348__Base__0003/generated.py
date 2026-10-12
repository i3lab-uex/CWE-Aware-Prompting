import requests
import hmac
from typing import Any, Dict

# Global mapping of user IDs to their expected signature (hex string)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; replace with real data
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "e99a18c428cb38d5f260853678922e03",
    # ...
}

def _fetch_profile(user_identifier: str) -> Dict[str, Any]:
    """
    Internal helper that retrieves the user profile from an external service.
    Raises requests.exceptions.RequestException on network errors or
    non‑200 HTTP status codes.
    """
    url = f"https://api.example.com/users/{user_identifier}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


def collect_user_data(user_identifier: str, user_signature: str) -> Dict[str, Any] | None:
    """
    Retrieve a user profile and verify its cryptographic signature.

    Parameters
    ----------
    user_identifier : str
        The identifier of the user whose profile is being fetched.
    user_signature : str
        The cryptographic signature attached to the profile data.

    Returns
    -------
    dict | None
        The user profile if signature verification succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    try:
        profile = _fetch_profile(user_identifier)
    except requests.exceptions.RequestException as exc:
        # Wrap lower‑level exceptions into a ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for {user_identifier}") from exc

    # Retrieve the expected signature for this user
    expected_signature = TRUSTED_USER_PROFILES.get(user_identifier)

    if not expected_signature:
        # No trusted signature known for this user
        return None

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(user_signature, expected_signature):
        return None

    return profile