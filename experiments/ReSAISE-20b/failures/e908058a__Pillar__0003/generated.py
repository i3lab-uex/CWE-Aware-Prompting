import json
import hmac
import hashlib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Global mapping of user IDs to their expected cryptographic signatures
TRUSTED_USER_PROFILES = {
    # Example entries (UUID: signature)
    "123e4567-e89b-12d3-a456-426614174000": "a1b2c3d4e5f6g7h8i9j0",
    # Add more trusted profiles here
}

def _fetch_profile_from_remote(uuid: str, timeout: float = 5.0) -> dict:
    """
    Fetch user profile JSON from a remote service.

    Raises:
        ConnectionError: if any network-related issue occurs.
    """
    # Example endpoint – replace with the real URL
    url = f"https://api.example.com/users/{uuid}/profile"
    req = Request(url, method="GET")
    try:
        with urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                raise ConnectionError(f"Unexpected status code {resp.status}")
            data = resp.read()
            return json.loads(data)
    except (URLError, HTTPError) as exc:
        raise ConnectionError(f"Failed to fetch profile for {uuid}") from exc

def collect_user_data(uuid: str, sig_hash: str) -> dict | None:
    """
    Retrieve a user profile and verify its cryptographic signature.

    Parameters
    ----------
    uuid : str
        The unique identifier of the user.
    sig_hash : str
        The cryptographic signature supplied with the profile data.

    Returns
    -------
    dict | None
        The user profile if the signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to connectivity problems.
    """
    # 1. Fetch the profile from the remote system
    profile = _fetch_profile_from_remote(uuid)

    # 2. Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if expected_sig is None:
        # No trusted signature available – treat as untrusted
        return None

    # 3. Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(sig_hash, expected_sig):
        # Signature mismatch – do not trust the data
        return None

    # 4. Return the trusted profile
    return profile