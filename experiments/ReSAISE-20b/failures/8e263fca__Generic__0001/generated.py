# -*- coding: utf-8 -*-
"""
Utility to fetch a user profile from a remote service and verify its signature.
"""

from __future__ import annotations

import json
import logging
from typing import Dict, Any, Optional

# Example trusted profiles dictionary.
# In a real system this would be loaded from secure storage or an external service.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "sig_alice_123",
    "bob": "sig_bob_456",
    # ... other trusted users ...
}

# Configure module‑level logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _simulate_remote_fetch(user_id: str) -> Dict[str, Any]:
    """
    Simulate a remote HTTP GET request to fetch user profile data.
    In production this would use `requests.get` or an async HTTP client.

    Parameters
    ----------
    user_id : str
        The unique identifier of the user.

    Returns
    -------
    dict
        Parsed JSON response representing the user's profile.

    Raises
    ------
    ConnectionError
        If the user cannot be found or network issues occur.
    """
    # For demonstration, assume every known user has a profile in the following format
    mock_profiles = {
        "alice": {"name": "Alice Smith", "age": 30, "email": "alice@example.com"},
        "bob": {"name": "Bob Jones", "age": 45, "email": "bob@example.com"},
    }

    if user_id not in mock_profiles:
        logger.debug("User %s not found during remote fetch.", user_id)
        raise ConnectionError(f"Unable to fetch profile for user '{user_id}'")

    # Simulate network latency
    logger.debug("Fetched profile for user %s successfully.", user_id)
    return mock_profiles[user_id]


def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Parameters
    ----------
    user_ident : str
        The unique identifier for the user whose profile is being fetched.
    user_sig : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    dict | None
        The user profile dictionary if signature matches, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the remote service.
    """
    # Step 1: Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if expected_sig is None:
        logger.warning(
            "User %s is not in the trusted profiles list. Rejecting request.",
            user_ident,
        )
        return None

    # Step 2: Compare signatures securely
    if not _constant_time_compare(user_sig, expected_sig):
        logger.warning(
            "Signature mismatch for user %s. Provided: %s, Expected: %s",
            user_ident,
            user_sig,
            expected_sig,
        )
        return None

    # Step 3: Attempt to fetch the profile from remote
    try:
        profile = _simulate_remote_fetch(user_ident)
    except ConnectionError as exc:
        logger.error("Failed to fetch profile for user %s: %s", user_ident, exc)
        raise

    logger.info("Profile for user %s fetched and verified.", user_ident)
    return profile


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Perform a constant‑time comparison of two strings to mitigate timing attacks.

    Parameters
    ----------
    val1 : str
        First value.
    val2 : str
        Second value.

    Returns
    -------
    bool
        ``True`` if the strings are identical, otherwise ``False``.
    """
    import hmac

    return hmac.compare_digest(val1.encode("utf-8"), val2.encode("utf-8"))


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    try:
        profile = fetch_profile_info("alice", "sig_alice_123")
        print("Fetched profile:", json.dumps(profile, indent=2))
    except ConnectionError as e:
        print("Connection error:", e)