import json
import urllib.request
import urllib.error
import hmac

# Example global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES = {
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user456": "e99a18c428cb38d5f260853678922e03",
    # ... other trusted users ...
}

def _fetch_profile(identifier: str) -> dict:
    """
    Internal helper that retrieves the user profile from a remote endpoint.
    Raises urllib.error.URLError on connectivity problems.
    """
    url = f"https://example.com/api/users/{identifier}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        if resp.status != 200:
            raise urllib.error.URLError(f"HTTP {resp.status}")
        data = resp.read()
    return json.loads(data.decode("utf-8"))

def access_user_details(identifier: str, crypt_sig: str):
    """
    Fetches a user profile and verifies the provided cryptographic signature.

    Parameters
    ----------
    identifier : str
        Unique user identifier.
    crypt_sig : str
        Cryptographic signature accompanying the profile data.

    Returns
    -------
    dict or None
        The user profile if signature verification succeeds; otherwise None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to network/connectivity issues.
    """
    try:
        profile = _fetch_profile(identifier)
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        # Wrap any URL related exception into a ConnectionError
        raise ConnectionError(f"Unable to fetch profile for {identifier}") from exc

    # Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)

    # If no signature is known for the user, treat as invalid
    if expected_sig is None:
        return None

    # Use constant‑time comparison to avoid timing attacks
    if hmac.compare_digest(crypt_sig, expected_sig):
        return profile

    # Signature mismatch
    return None