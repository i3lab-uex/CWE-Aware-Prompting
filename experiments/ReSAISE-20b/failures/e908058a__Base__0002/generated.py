import json
import hashlib
import urllib.request
from urllib.error import URLError, HTTPError

# Global dictionary mapping user IDs to their correct cryptographic signatures
TRUSTED_USER_PROFILES = {
    # Example entries – replace with real data in production
    "user-123": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd3b4c8f9e2",
    "user-456": "d8578edf8458ce06fbc5bb76a58c5",
    # ...
}

def collect_user_data(uuid: str, sig_hash: str):
    """
    Fetch a user profile from a remote system and verify its cryptographic signature.

    Parameters
    ----------
    uuid : str
        Unique identifier for the user whose profile needs to be fetched.
    sig_hash : str
        Cryptographic signature provided with the profile data.

    Returns
    -------
    dict | None
        The parsed JSON profile if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a network or connectivity issue.
    """
    # The remote endpoint – adjust the URL as appropriate
    url = f"https://api.example.com/users/{uuid}/profile"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            if resp.status != 200:
                raise ConnectionError(f"Unexpected HTTP status {resp.status}")
            raw_data = resp.read()
    except (URLError, HTTPError) as exc:
        # Wrap lower‑level network errors in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for {uuid}") from exc

    # Parse JSON data
    try:
        profile = json.loads(raw_data.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON received for {uuid}") from exc

    # Verify the signature using SHA-256 over the canonical JSON representation
    profile_json = json.dumps(profile, sort_keys=True, separators=(",", ":"))
    computed_hash = hashlib.sha256(profile_json.encode("utf-8")).hexdigest()

    # Check against the expected signature from the trusted list
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if expected_sig is None:
        # Unknown user – treat as untrusted
        return None

    if computed_hash != expected_sig:
        # Signature mismatch – data is not trustworthy
        return None

    # Signature verified; return the profile
    return profile