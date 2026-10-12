import json
import secrets
from urllib import request, error

# Example trusted signatures (user_id -> expected signature)
TRUSTED_USER_PROFILES = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted users here
}

def _fetch_remote_profile(user_ident: str) -> dict:
    """
    Simulates a remote HTTP request to fetch the user profile.
    Raises ConnectionError on network failure or non‑200 status codes.
    """
    # In a real implementation this would be something like:
    # url = f"https://api.example.com/users/{user_ident}"
    # req = request.Request(url, headers={"Accept": "application/json"})
    #
    # For this example we use a mock URL that always returns 200
    # or raises an error to demonstrate the exception handling.
    url = f"https://mock.service/users/{user_ident}"
    try:
        with request.urlopen(url, timeout=5) as resp:
            if resp.status != 200:
                raise ConnectionError(f"Unexpected status {resp.status}")
            data = resp.read()
            return json.loads(data)
    except error.URLError as exc:
        raise ConnectionError(f"Failed to fetch profile: {exc}") from exc

def fetch_profile_info(user_ident: str, user_sig: str) -> dict | None:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Parameters
    ----------
    user_ident : str
        Unique identifier for the user.
    user_sig : str
        Cryptographic signature provided with the profile.

    Returns
    -------
    dict | None
        The user profile if the signature matches the trusted value,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the remote service.
    """
    # Fetch the profile; propagate any connection errors
    profile = _fetch_remote_profile(user_ident)

    # Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if expected_sig is None:
        # User not recognized; treat as untrusted
        return None

    # Use secrets.compare_digest to avoid timing attacks
    if not secrets.compare_digest(user_sig, expected_sig):
        # Signature mismatch – reject the profile
        return None

    # All checks passed; return the trusted profile
    return profile