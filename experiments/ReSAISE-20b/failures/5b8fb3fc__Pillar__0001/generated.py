import hashlib
import hmac
import json
from typing import Dict, Optional

# Global dictionary mapping user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user1": "a3f5c2e7d9b8f6a4e1c0d3b2",
    "user2": "5d7e9a1b6c4f3e8d0b2a9c5f",
    # Add more trusted users as needed
}

def _fetch_profile_from_remote(uid: str) -> Dict:
    """
    Simulate fetching a user profile from a remote service.
    In a real implementation this would perform an HTTP request.

    Raises:
        ConnectionError: If the remote service cannot be reached.
    """
    # For demonstration purposes we pretend that the profile is stored locally.
    # In production, replace this with an actual network call.
    simulated_remote_db = {
        "user1": {"name": "Alice", "email": "alice@example.com"},
        "user2": {"name": "Bob", "email": "bob@example.com"},
    }

    # Simulate a connection failure for unknown users
    if uid not in simulated_remote_db:
        raise ConnectionError(f"Unable to reach remote service for UID: {uid}")

    return simulated_remote_db[uid]


def _verify_signature(uid: str, provided_sig: str) -> bool:
    """
    Verify that the provided signature matches the expected one for the given UID.
    Uses constant‑time comparison to mitigate timing attacks.

    Returns:
        True if signatures match, False otherwise.
    """
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # Unknown user; treat as invalid signature
        return False

    # Ensure both signatures are byte strings for compare_digest
    provided_bytes = provided_sig.encode("utf-8")
    expected_bytes = expected_sig.encode("utf-8")

    return hmac.compare_digest(provided_bytes, expected_bytes)


def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict]:
    """
    Retrieve a user profile from a remote service after verifying its cryptographic signature.

    Args:
        uid: The unique identifier for the user whose profile is being fetched.
        sig: The cryptographic signature associated with the user profile.

    Returns:
        The user profile dictionary if the signature is valid; otherwise None.

    Raises:
        ConnectionError: If it's not possible to fetch the profile from the remote service.
    """
    # Step 1: Verify the signature before any network call
    if not _verify_signature(uid, sig):
        return None

    # Step 2: Fetch the profile from the remote service
    try:
        profile = _fetch_profile_from_remote(uid)
    except ConnectionError as exc:
        # Re‑raise to signal failure to the caller
        raise exc

    return profile


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        profile = retrieve_user_profile("user1", "a3f5c2e7d9b8f6a4e1c0d3b2")
        print("Profile retrieved:", profile)
    except ConnectionError as e:
        print("Failed to retrieve profile:", e)