import json
from typing import Any, Optional

import requests
from hmac import compare_digest

# Global mapping of user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: dict[str, str] = {
    "alice": "d41d8cd98f00b204e9800998ecf8427e",
    "bob":   "0cc175b9c0f1b6a831c399e269772661",
    # Add more trusted user IDs and signatures as needed.
}

def retrieve_user_info(uid: str, sig: str) -> Optional[dict[str, Any]]:
    """
    Retrieve a user profile from the remote system and verify its authenticity.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    sig : str
        Cryptographic signature that accompanies the profile data.

    Returns
    -------
    dict | None
        The user profile if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a connectivity issue.
    """
    # Step 1: Fetch the user profile from the remote API.
    url = f"https://api.example.com/users/{uid}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Convert any request‑related error into a ConnectionError.
        raise ConnectionError(f"Failed to fetch user profile for {uid}") from exc

    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # If the payload isn't valid JSON, treat it as a connectivity/formatting issue.
        raise ConnectionError(f"Invalid response format for user {uid}") from exc

    # Step 2: Verify the signature.
    # The trusted signature for this user is retrieved from the global mapping.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # Unknown user ID – treat as untrusted.
        return None

    # Use constant‑time comparison to avoid timing attacks.
    if not compare_digest(sig, expected_sig):
        return None

    # Signature is valid; return the profile data.
    return profile_data