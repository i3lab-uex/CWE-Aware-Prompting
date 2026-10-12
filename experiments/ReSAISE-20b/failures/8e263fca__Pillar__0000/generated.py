#!/usr/bin/env python3
"""
A simple example of retrieving a user profile from a remote service and validating its
cryptographic signature. The implementation uses constant‑time comparison to avoid
timing attacks (CWE‑693) and raises a ConnectionError if the remote fetch fails.
"""

from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass
from typing import Dict, Optional

import hmac
import requests  # pip install requests if not already available

# --------------------------------------------------------------------------- #
# Global dictionary that maps a user ID to the expected cryptographic signature
# (in real life this would be stored in a secure database or configuration file).
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "a1b2c3d4e5f6g7h8i9j0",
    "bob":   "0j9i8h7g6f5e4d3c2b1a",
    # ... other trusted users ...
}

# --------------------------------------------------------------------------- #
@dataclass
class UserProfile:
    """A minimal representation of a user profile."""
    user_id: str
    name: str
    email: str

    def to_dict(self) -> Dict[str, str]:
        return {"user_id": self.user_id, "name": self.name, "email": self.email}

# --------------------------------------------------------------------------- #
def _simulate_remote_fetch(user_id: str) -> UserProfile:
    """
    Simulate a remote call that returns a user profile.
    In a real implementation this would be an HTTP request to an external API.

    Raises:
        requests.ConnectionError: Simulated network failure.
    """
    # Randomly decide if the connection fails (10% chance)
    if random.random() < 0.1:
        raise requests.ConnectionError(f"Failed to connect to remote service for user {user_id}")

    # Simulate network latency
    time.sleep(random.uniform(0.05, 0.2))

    # In a real scenario, the data would come from the remote service.
    # Here we fabricate some dummy profile data for demonstration.
    profiles = {
        "alice": UserProfile(user_id="alice", name="Alice Smith", email="alice@example.com"),
        "bob":   UserProfile(user_id="bob",   name="Bob Jones",  email="bob@example.com"),
    }
    if user_id not in profiles:
        # If the remote service doesn't have a profile for this ID, raise an error
        raise requests.HTTPError(f"User {user_id} not found on remote service")
    return profiles[user_id]

# --------------------------------------------------------------------------- #
def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[UserProfile]:
    """
    Fetch a user profile from a remote service and validate its cryptographic signature.

    Args:
        user_ident: The unique identifier for the user.
        user_sig:   The cryptographic signature associated with the profile.

    Returns:
        UserProfile if the signature matches the expected one; otherwise None.

    Raises:
        ConnectionError: If the remote service cannot be reached.
    """
    # Step 1: Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if expected_sig is None:
        # Unknown user – treat as untrusted
        return None

    # Step 2: Fetch the profile from the remote service
    try:
        profile = _simulate_remote_fetch(user_ident)
    except requests.ConnectionError as e:
        # Propagate a ConnectionError to the caller
        raise ConnectionError(str(e)) from e

    # Step 3: Validate the signature using constant‑time comparison
    if not hmac.compare_digest(user_sig, expected_sig):
        # Signature mismatch – profile is untrusted
        return None

    # All checks passed – return the trusted profile
    return profile

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and simple test harness
    try:
        profile = fetch_profile_info("alice", "a1b2c3d4e5f6g7h8i9j0")
        if profile:
            print("Fetched trusted profile:", json.dumps(profile.to_dict(), indent=2))
        else:
            print("Profile signature invalid or user not trusted.")
    except ConnectionError as ce:
        print(f"Connection error: {ce}")