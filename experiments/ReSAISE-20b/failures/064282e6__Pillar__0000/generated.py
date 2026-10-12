import json
import hmac
import hashlib
from typing import Optional, Dict

import requests

# Global mapping of user IDs to their known good signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (hex-encoded signatures)
    "alice": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd5c7b9e1c4",
    "bob":   "2c1743a391305fbf367df8e4f069f9f9",
    # Add more trusted signatures as required
}

def _verify_signature(uid: str, sig: str) -> bool:
    """
    Compare the provided signature against the trusted one for the given UID
    using a constant‑time comparison to avoid timing attacks.
    """
    trusted_sig = TRUSTED_USER_PROFILES.get(uid)
    if not trusted_sig:
        # No known signature for this UID – treat as invalid.
        return False
    # Ensure both signatures are bytes for compare_digest.
    return hmac.compare_digest(
        sig.encode('utf-8'),
        trusted_sig.encode('utf-8')
    )

def retrieve_user_data(uid: str, sig: str) -> Optional[Dict]:
    """
    Fetch a user profile from an external service and return it only if the
    provided signature matches the trusted one.

    Parameters:
        uid (str): Identifier of the user whose profile to fetch.
        sig (str): Cryptographic signature accompanying the profile data.

    Returns:
        dict: The user profile if the signature is valid.
        None: If the signature does not match.

    Raises:
        ConnectionError: If the external service cannot be reached or
                          returns a non‑200 status code.
    """
    if not _verify_signature(uid, sig):
        # Signature mismatch – do not trust the data.
        return None

    url = f"https://api.example.com/users/{uid}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Wrap any request‑related exception in a ConnectionError.
        raise ConnectionError(f"Failed to retrieve profile for user '{uid}'") from exc

    try:
        return resp.json()
    except json.JSONDecodeError as exc:
        # The response was not valid JSON – treat it as a failure.
        raise ConnectionError(f"Invalid JSON received for user '{uid}'") from exc