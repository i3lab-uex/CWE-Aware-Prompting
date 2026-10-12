#!/usr/bin/env python3
"""
Secure user profile retrieval with signature validation.

This module demonstrates a safe implementation of the `get_user_details` function,
addressing CWE‑693 by properly validating the cryptographic signature and
handling errors correctly.

Author: ChatGPT
"""

from __future__ import annotations

import hmac
import json
import random
import time
from typing import Dict, Optional

# --------------------------------------------------------------------------- #
# Global data
# --------------------------------------------------------------------------- #

# Mapping of user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted users here.
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _simulate_remote_fetch(u_id: str) -> Dict[str, str]:
    """
    Simulate a network call to fetch user profile data.

    The function randomly fails to emulate network unreliability.
    In a real implementation this would be replaced with an HTTP request
    (e.g., using `requests` or `http.client`) to a remote service.

    Parameters
    ----------
    u_id : str
        The user identifier whose profile is to be fetched.

    Returns
    -------
    Dict[str, str]
        A dictionary representing the user's profile.

    Raises
    ------
    ConnectionError
        If the simulated network call fails.
    """
    # Simulate latency
    time.sleep(random.uniform(0.05, 0.2))

    # Simulate a 10% chance of network failure
    if random.random() < 0.1:
        raise ConnectionError(f"Unable to reach remote service for user {u_id!r}")

    # Return a dummy profile (in real life this would come from the remote service)
    return {
        "u_id": u_id,
        "name": f"User {u_id.capitalize()}",
        "email": f"{u_id}@example.com",
    }

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def get_user_details(u_id: str, sig_code: str) -> Optional[Dict[str, str]]:
    """
    Retrieve a user profile from a remote service and validate its cryptographic signature.

    Parameters
    ----------
    u_id : str
        The unique identifier for the user whose profile is being fetched.
    sig_code : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    Optional[Dict[str, str]]
        The user profile dictionary if the signature is valid; otherwise `None`.

    Raises
    ------
    ConnectionError
        If it is impossible to fetch the profile from the remote service.
    """
    # Step 1: Retrieve expected signature for this user (if any)
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)

    # If the user is not in our trusted list, we consider the signature invalid.
    if expected_sig is None:
        return None

    # Step 2: Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(sig_code, expected_sig):
        return None

    # Step 3: Fetch the profile from the remote service
    try:
        profile = _simulate_remote_fetch(u_id)
    except ConnectionError as exc:
        # Re‑raise the exception so callers can handle it appropriately
        raise

    # Step 4: Return the verified profile
    return profile


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example: Alice with correct signature
    try:
        alice_profile = get_user_details("alice", "5f4dcc3b5aa765d61d8327deb882cf99")
        print("Alice profile:", json.dumps(alice_profile, indent=2))
    except ConnectionError as e:
        print("Failed to fetch Alice:", e)

    # Example: Bob with incorrect signature
    bob_profile = get_user_details("bob", "incorrect_signature")
    print("Bob profile (should be None):", bob_profile)