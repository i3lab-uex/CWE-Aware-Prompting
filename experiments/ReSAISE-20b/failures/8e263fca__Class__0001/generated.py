import json
import hmac
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Mapping of user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "f3a9c2e1d4b8...",
    "bob":   "5c7f9a3b2e1d4...",
    # Add more trusted users here.
}

# Base URL of the remote profile service (replace with actual endpoint).
PROFILE_SERVICE_URL = "https://api.example.com/user/profile"


def _fetch_remote_profile(user_ident: str) -> Dict[str, Any]:
    """
    Internal helper that performs the HTTP GET request to retrieve
    the user profile. Raises ConnectionError on any network failure.
    """
    try:
        response = requests.get(
            f"{PROFILE_SERVICE_URL}/{user_ident}",
            timeout=5.0,  # seconds
        )
        response.raise_for_status()
    except RequestException as exc:
        raise ConnectionError(f"Unable to fetch profile for user '{user_ident}'.") from exc

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON returned for user '{user_ident}'.") from exc


def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the remote service and validate its
    cryptographic signature.

    Parameters:
        user_ident (str): Unique identifier of the user.
        user_sig (str):   Signature accompanying the profile data.

    Returns:
        dict: The user profile if signature matches.
        None: If the signature does not match or the user is unknown.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # Step 1: Retrieve the expected signature for this user (if any).
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if expected_sig is None:
        # Unknown user; treat as untrusted.
        return None

    # Step 2: Perform constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(user_sig, expected_sig):
        return None

    # Step 3: Fetch the profile from the remote service.
    profile = _fetch_remote_profile(user_ident)

    # Optional: Additional sanity checks on the profile structure could be added here.

    return profile