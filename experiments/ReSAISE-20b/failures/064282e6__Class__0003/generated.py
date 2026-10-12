import hashlib
import hmac
import random
import time
from typing import Dict, Any

# Example global dictionary containing trusted signatures for each user.
# In a real system this would be populated from a secure source such as
# a database, HSM or an external key‑management service.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # uid : signature (hex digest of the profile data)
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "e99a18c428cb38d5f260853678922e03",
}

# Simulated external service endpoint (normally this would be a URL)
EXTERNAL_SERVICE_ENDPOINT = "https://api.example.com/user_profile"


def _fetch_from_external_service(uid: str) -> Dict[str, Any]:
    """
    Simulate a network call to fetch the user profile data.
    In production this would use `requests.get` or similar.

    Raises:
        ConnectionError: If the network call fails.
    """
    # Randomly simulate a connection failure
    if random.random() < 0.1:   # 10% chance of failure
        raise ConnectionError(f"Failed to connect to {EXTERNAL_SERVICE_ENDPOINT}")

    # Simulate network latency
    time.sleep(random.uniform(0.05, 0.2))

    # Dummy profile data; in a real system this would be the JSON payload.
    profiles = {
        "alice": {"uid": "alice", "name": "Alice Smith", "email": "alice@example.com"},
        "bob":   {"uid": "bob",   "name": "Bob Jones",  "email": "bob@example.com"},
    }
    return profiles.get(uid, {})


def _compute_signature(data: Dict[str, Any]) -> str:
    """
    Compute a deterministic signature for the profile data.
    Here we use SHA‑256 over the JSON string representation.  In
    production a proper cryptographic signature scheme (e.g.
    RSA/ECDSA) should be used.

    Returns:
        str: Hexadecimal digest of the signature.
    """
    # Convert dictionary to a sorted JSON string for deterministic hashing
    import json

    payload = json.dumps(data, sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    return digest


def retrieve_user_data(uid: str, sig: str) -> Dict[str, Any] | None:
    """
    Retrieve a user profile from an external service and validate the
    supplied signature against the trusted value.

    Args:
        uid: The user identifier to fetch.
        sig: Cryptographic signature claimed for the profile data.

    Returns:
        The user profile dictionary if verification succeeds, otherwise None.

    Raises:
        ConnectionError: If the external service cannot be reached.
    """
    # 1. Fetch profile data from external source
    try:
        profile_data = _fetch_from_external_service(uid)
    except ConnectionError as e:
        # Propagate the connection error
        raise

    if not profile_data:
        # No data returned for this UID; treat as failure to retrieve
        raise ConnectionError(f"No profile found for user '{uid}'")

    # 2. Compute the expected signature
    expected_sig = _compute_signature(profile_data)

    # 3. Verify that the provided signature matches the trusted one
    trusted_sig = TRUSTED_USER_PROFILES.get(uid)
    if not trusted_sig:
        # No trusted signature known for this user
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE-345)
    if not hmac.compare_digest(sig, trusted_sig):
        return None

    # 4. Return the verified profile
    return profile_data


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    # Prepare a signature for Alice (using the same algorithm as in _compute_signature)
    alice_profile = _fetch_from_external_service("alice")
    alice_sig = _compute_signature(alice_profile)

    # Retrieve with correct signature
    print(retrieve_user_data("alice", alice_sig))

    # Attempt retrieval with an invalid signature
    print(retrieve_user_data("alice", "invalidsignature"))