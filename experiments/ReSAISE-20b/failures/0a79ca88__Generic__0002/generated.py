import json
import requests
from typing import Optional, Dict

# Global mapping of user IDs to their trusted cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted users here.
}

def get_user_details(u_id: str, sig_code: str) -> Optional[Dict]:
    """
    Retrieve a user profile from a remote service and verify its cryptographic signature.

    Parameters
    ----------
    u_id : str
        Unique identifier for the user.
    sig_code : str
        Cryptographic signature provided with the profile.

    Returns
    -------
    dict or None
        The user profile dictionary if the signature matches a trusted one,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the remote service cannot be reached or returns a non-success status.
    """
    # Ensure inputs are strings to avoid injection attacks
    if not isinstance(u_id, str) or not isinstance(sig_code, str):
        raise ValueError("Both u_id and sig_code must be strings.")

    # Construct the request URL (placeholder)
    url = f"https://api.example.com/users/{u_id}"

    try:
        # Perform the HTTP GET request with a timeout.
        response = requests.get(url, timeout=5)
    except (requests.exceptions.RequestException, OSError) as exc:
        # Wrap any request/OS error into a ConnectionError
        raise ConnectionError(f"Failed to fetch user profile: {exc}") from exc

    if response.status_code != 200:
        raise ConnectionError(
            f"Remote service returned unexpected status {response.status_code}"
        )

    try:
        profile = response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError("Response was not valid JSON") from exc

    # Verify that the provided signature matches the trusted one.
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if not expected_sig or sig_code != expected_sig:
        return None

    # All checks passed; return the profile.
    return profile