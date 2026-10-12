import requests
from typing import Any, Dict, Optional

# Global mapping of user IDs to their expected signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – replace with real data.
    "alice": "5f2b8c9e1d3a4b6c7d8e9f0a1b2c3d4e",
    "bob":   "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p",
}

def retrieve_user_data(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and validate its signature.

    Parameters
    ----------
    uid : str
        Identifier of the target user.
    sig : str
        Cryptographic signature attached to the profile data.

    Returns
    -------
    dict | None
        The user profile data if the signature is verified; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the external service cannot be reached or returns an error status.
    """
    # Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # No trusted signature known – we cannot trust any data for this UID.
        return None

    # Quick check: if the provided signature does not match the expected one,
    # we reject immediately.  This is a simple security measure; in a real
    # system you would perform cryptographic verification (e.g., RSA/ECDSA).
    if sig != expected_sig:
        return None

    # Build the URL to fetch the profile.  Replace with the real endpoint.
    url = f"https://api.example.com/users/{uid}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Wrap network-related errors into a ConnectionError for the caller.
        raise ConnectionError(f"Failed to retrieve profile for UID {uid}") from exc

    # Assuming the service returns JSON.
    try:
        profile_data = response.json()
    except ValueError as exc:
        # The payload was not valid JSON.
        raise ConnectionError(f"Invalid response format for UID {uid}") from exc

    # In a real-world scenario, you would validate the signature against the
    # content of `profile_data` here (e.g., using a public key).  Since we
    # already matched the expected signature, we simply return the data.
    return profile_data