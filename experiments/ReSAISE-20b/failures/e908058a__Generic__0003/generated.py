import json
import ssl
from urllib import request, error
from typing import Optional

# Global dictionary mapping user IDs to the expected signature hash.
TRUSTED_USER_PROFILES = {
    # Example entries; replace with actual trusted signatures.
    "user-1234": "a1b2c3d4e5f6g7h8i9j0",
    "user-5678": "deadbeefcafebabe1234",
}

def _fetch_profile_from_remote(uuid: str, timeout: float = 5.0) -> dict:
    """
    Helper that performs the actual HTTP GET request to fetch user profile data.
    It uses HTTPS with certificate validation and a reasonable timeout.

    Args:
        uuid: The user ID to request.
        timeout: Timeout in seconds for the request.

    Returns:
        Parsed JSON response as a dictionary.

    Raises:
        ConnectionError: If the request fails due to network or SSL issues.
    """
    url = f"https://api.example.com/users/{uuid}/profile"
    req = request.Request(url, method="GET")
    # Ensure we use a secure SSL context
    ctx = ssl.create_default_context()
    try:
        with request.urlopen(req, timeout=timeout, context=ctx) as resp:
            if resp.status != 200:
                raise ConnectionError(f"Unexpected status code {resp.status}")
            data = resp.read()
            return json.loads(data.decode("utf-8"))
    except (error.URLError, error.HTTPError, ssl.SSLError) as exc:
        raise ConnectionError(f"Failed to fetch profile for {uuid}: {exc}") from exc

def collect_user_data(uuid: str, sig_hash: str) -> Optional[dict]:
    """
    Obtain a user profile from the remote system and verify its cryptographic signature.

    Args:
        uuid: Unique identifier for the user.
        sig_hash: Cryptographic signature provided with the profile data.

    Returns:
        The user profile dictionary if the signature is valid; otherwise, None.

    Raises:
        ConnectionError: If fetching the profile fails due to connectivity issues.
    """
    # Verify signature against trusted list first (quick rejection)
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if not expected_sig:
        # Unknown user; consider this a failure to prevent leaking info
        return None

    if sig_hash != expected_sig:
        # Signature mismatch; do not trust the data
        return None

    # Fetch profile only if signature is trusted
    profile = _fetch_profile_from_remote(uuid)

    # Optional: Additional sanity checks on the profile content can be added here
    return profile