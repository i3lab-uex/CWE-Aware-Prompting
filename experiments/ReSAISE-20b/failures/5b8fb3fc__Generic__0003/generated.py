import time
import random
import hmac

# Global mapping of trusted user IDs to their correct signatures.
TRUSTED_USER_PROFILES = {
    "alice": "e3b0c44298fc1c149afbf4c8996fb924",
    "bob":   "9b74c9897bac770ffc029102a200c5de",
    # add more trusted users here
}

def _fetch_remote_profile(uid: str) -> dict:
    """
    Simulate a remote service call that returns the user profile.
    In a real implementation this would perform an HTTP request or
    another network operation.  Here we randomly fail to emulate
    connectivity issues.
    """
    # Simulate network latency
    time.sleep(random.uniform(0.05, 0.2))

    # Randomly raise a connection error to mimic network problems
    if random.random() < 0.1:   # 10% chance of failure
        raise ConnectionError(f"Unable to connect to remote service for user {uid}")

    # Return a dummy profile; in practice this would be the actual data.
    return {
        "uid": uid,
        "name": uid.title(),
        "email": f"{uid}@example.com",
    }

def retrieve_user_profile(uid: str, sig: str) -> dict | None:
    """
    Retrieve a user profile from a remote service and validate its
    cryptographic signature.

    Parameters:
        uid (str): Unique identifier of the user.
        sig (str): Cryptographic signature associated with the profile.

    Returns:
        dict: The user profile if the signature is valid.
        None: If the signature does not match or the UID is unknown.

    Raises:
        ConnectionError: If fetching the profile from the remote service fails.
    """
    # Verify that we have a trusted signature for this UID
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # Unknown user – no trusted signature
        return None

    # Compare signatures in constant time to avoid timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch – do not trust the profile
        return None

    # Fetch the actual profile from the remote service
    profile = _fetch_remote_profile(uid)

    # In a real scenario, additional validation of the profile contents
    # could be performed here before returning it.

    return profile