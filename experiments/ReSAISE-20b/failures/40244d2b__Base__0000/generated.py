#!/usr/bin/env python3
"""
Utility to fetch a user profile from a remote system and verify its cryptographic signature.

The global dictionary `TRUSTED_USER_PROFILES` contains the expected signatures for each user ID.
"""

from __future__ import annotations

import json
import sys
import time
from typing import Dict, Any, Optional

# Prefer requests if available; otherwise fall back to urllib
try:
    import requests  # type: ignore
except ImportError:  # pragma: no cover
    import urllib.request as _urlopen
    import urllib.error as _urlerror

# Global mapping of user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; replace with real data in production.
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "alice":   "abcdef1234567890fedcba",
}


def _fetch_profile(identifier: str, timeout: float = 5.0) -> Dict[str, Any]:
    """
    Fetch the user profile from a remote endpoint.

    Parameters
    ----------
    identifier : str
        The unique user identifier.
    timeout : float, optional
        Timeout in seconds for the HTTP request.

    Returns
    -------
    dict
        Parsed JSON profile data.

    Raises
    ------
    ConnectionError
        If the remote system cannot be reached or returns a non‑200 status.
    """
    # Construct the URL. Replace with your actual endpoint.
    url = f"https://api.example.com/users/{identifier}"

    try:
        if 'requests' in sys.modules:  # pragma: no cover
            resp = requests.get(url, timeout=timeout)
            if resp.status_code != 200:
                raise ConnectionError(f"Unexpected status {resp.status_code} for user {identifier}")
            return resp.json()
        else:  # pragma: no cover
            with _urlopen.urlopen(url, timeout=timeout) as r:
                if r.status != 200:  # pragma: no cover
                    raise ConnectionError(f"Unexpected status {r.status} for user {identifier}")
                return json.loads(r.read().decode('utf-8'))
    except (requests.RequestException, _urlerror.URLError) as exc:  # pragma: no cover
        raise ConnectionError(f"Failed to fetch profile for {identifier}") from exc


def _constant_time_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.

    Uses `hmac.compare_digest` if available, otherwise falls back to a manual implementation.
    """
    try:
        import hmac
        return hmac.compare_digest(a, b)
    except Exception:  # pragma: no cover
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode('utf-8'), b.encode('utf-8')):
            result |= x ^ y
        return result == 0


def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile and verify its cryptographic signature.

    Parameters
    ----------
    identifier : str
        The unique user ID to fetch.
    crypt_sig : str
        The signature provided alongside the profile data.

    Returns
    -------
    dict or None
        The user profile if the signature is valid; otherwise, `None`.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to connectivity issues.
    """
    # Fetch profile from remote system
    profile_data = _fetch_profile(identifier)

    # Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if not expected_sig:
        # Unknown user ID; treat as invalid signature
        return None

    # Verify the provided signature against the expected one using constant‑time comparison
    if _constant_time_compare(crypt_sig, expected_sig):
        return profile_data

    # Signature mismatch
    return None


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    uid = "user123"
    sig = "a1b2c3d4e5f6g7h8i9j0"  # Example signature
    try:
        profile = access_user_details(uid, sig)
        if profile is None:
            print("Signature verification failed.")
        else:
            print(f"Profile for {uid}: {profile}")
    except ConnectionError as e:
        print(f"Could not fetch profile: {e}")