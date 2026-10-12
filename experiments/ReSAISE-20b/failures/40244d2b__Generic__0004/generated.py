import json
from typing import Any, Dict, Optional

try:
    # Use the standard library only – no external dependencies
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
except Exception:
    # Fallback for environments where the standard library is limited
    raise ImportError("Required modules for HTTP access are missing")

# Global dictionary mapping user IDs to their trusted cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – replace with actual trusted signatures
    "user123": "abcdef123456",
    "alice":   "123abc789def",
}

def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from a remote system and verify its cryptographic signature.

    Parameters
    ----------
    identifier : str
        Unique user identifier.
    crypt_sig : str
        Cryptographic signature supplied with the profile data.

    Returns
    -------
    dict or None
        The parsed JSON profile if the signature is valid; otherwise None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a connectivity issue.
    """
    # First, verify the signature against the trusted list
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if expected_sig is None or crypt_sig != expected_sig:
        # Either the user ID is unknown or the signature does not match
        return None

    # Construct a secure HTTPS URL for fetching the profile
    url = f"https://api.example.com/users/{identifier}"
    req = Request(url, headers={"Accept": "application/json"})

    try:
        with urlopen(req, timeout=10) as response:  # 10‑second timeout
            if response.status != 200:
                raise ConnectionError(f"Unexpected HTTP status {response.status}")
            data = response.read()
    except (URLError, HTTPError) as exc:
        # Any network-related error is treated as a connectivity issue
        raise ConnectionError(f"Failed to fetch user profile: {exc}") from exc

    # Parse JSON safely
    try:
        profile = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If the response is not valid JSON, treat it as a failure
        return None

    return profile