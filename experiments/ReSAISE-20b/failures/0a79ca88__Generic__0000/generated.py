import json
import urllib.request
import urllib.error
import random
from typing import Optional, Dict

# Simulated database of trusted signatures for user profiles.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "alice":   "deadbeef12345678",
    "bob":     "feedface87654321",
}

# Base URL of the remote service that returns user profiles in JSON format.
REMOTE_SERVICE_BASE_URL = "https://example.com/api/user/"

def _fetch_profile_from_remote(u_id: str) -> dict:
    """
    Fetch a user profile from the remote service.

    The function simulates network unreliability by randomly raising
    a ConnectionError. In a real implementation, this would perform an
    HTTP GET request to the remote API.
    """
    # Simulate network failure with a 10% chance
    if random.random() < 0.1:
        raise ConnectionError(f"Failed to connect to remote service for user {u_id}")

    # Simulated response (in reality you would use urllib.request.urlopen or requests.get)
    url = f"{REMOTE_SERVICE_BASE_URL}{u_id}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = response.read()
            return json.loads(data.decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # User not found; return empty dict
            return {}
        raise ConnectionError(f"HTTP error {e.code} when fetching profile for user {u_id}") from e
    except urllib.error.URLError as e:
        raise ConnectionError(f"URL error when fetching profile for user {u_id}") from e

def get_user_details(u_id: str, sig_code: str) -> Optional[dict]:
    """
    Retrieve a user profile from the remote service and validate its signature.

    Parameters
    ----------
    u_id : str
        The unique identifier of the user.
    sig_code : str
        Cryptographic signature associated with the user's profile.

    Returns
    -------
    dict or None
        The user profile if the signature matches the trusted value;
        otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # First, check that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if not expected_sig:
        # Unknown user or no trusted signature
        return None

    # Ensure the provided signature matches the expected one.
    if sig_code != expected_sig:
        return None

    # Fetch the profile from the remote service
    profile = _fetch_profile_from_remote(u_id)

    # If the profile is empty, treat it as not found
    if not profile:
        return None

    # Optionally, you might want to add extra validation on the profile contents here.

    return profile