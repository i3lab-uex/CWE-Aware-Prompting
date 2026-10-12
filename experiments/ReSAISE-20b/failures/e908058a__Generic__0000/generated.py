import json
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global mapping of user IDs to their trusted signature hashes.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (replace with real data in production)
    "user-123": "abcde12345fghij67890klmnop",
    "user-456": "98765zyxwvutsrq3210ponmlk",
}

def collect_user_data(uuid: str, sig_hash: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the remote system and verify its signature.

    Parameters
    ----------
    uuid : str
        Unique identifier for the user whose profile is to be fetched.
    sig_hash : str
        Cryptographic signature provided with the profile data.

    Returns
    -------
    dict | None
        The user profile JSON object if the signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a network/connectivity problem.
    """
    # Validate that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if not expected_sig:
        # Unknown user – we cannot trust any data for them
        return None

    # Quick pre‑check: if the supplied signature doesn't match what we expect,
    # skip the network call entirely.
    if sig_hash != expected_sig:
        return None

    # Construct the request URL.  In a real implementation this would point to
    # the actual service endpoint.
    url = f"https://api.example.com/users/{uuid}"

    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any requests exception in a ConnectionError to match the spec.
        raise ConnectionError(f"Failed to fetch profile for user {uuid}") from exc

    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        # If the payload is not valid JSON we treat it as a failure to fetch.
        raise ConnectionError(f"Invalid JSON response for user {uuid}") from exc

    # At this point we already verified the signature earlier, but if you
    # want to double‑check against a server-provided hash you could add it here.
    return data