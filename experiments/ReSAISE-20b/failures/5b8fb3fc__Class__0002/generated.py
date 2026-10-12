import hmac
import hashlib
import random
import time

# Global mapping of user IDs to their correct cryptographic signatures.
TRUSTED_USER_PROFILES = {
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "alice":   "deadbeefcafebabe1234",
    # Add more trusted user profiles here
}

def _fetch_remote_profile(uid: str) -> dict:
    """
    Simulate fetching a user profile from a remote service.

    In a real implementation this would perform an HTTP request or similar.
    For the purposes of this example we simply return a dummy profile after
    a short delay. Randomly raise ConnectionError to emulate network issues.
    """
    # Simulate network latency
    time.sleep(0.05)

    # Randomly fail to mimic unreliable network
    if random.random() < 0.05:   # 5% chance of failure
        raise ConnectionError(f"Unable to fetch profile for UID {uid}")

    # Dummy profile data
    return {
        "uid": uid,
        "name": f"User {uid}",
        "email": f"{uid}@example.com",
    }

def retrieve_user_profile(uid: str, sig: str) -> dict | None:
    """
    Retrieve a user profile from a remote service and validate its cryptographic
    signature against the trusted value.

    Parameters:
        uid (str): The unique identifier of the user.
        sig (str): The cryptographic signature provided for validation.

    Returns:
        dict | None: The user profile dictionary if the signature is valid;
                     otherwise, None.

    Raises:
        ConnectionError: If fetching the profile from the remote service fails.
    """
    # Step 1: Fetch the profile
    profile = _fetch_remote_profile(uid)

    # Step 2: Retrieve the expected signature for this UID
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # Unknown UID – cannot trust the profile
        return None

    # Step 3: Constant‑time comparison to prevent timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch – reject the profile
        return None

    # Step 4: Return the trusted profile
    return profile