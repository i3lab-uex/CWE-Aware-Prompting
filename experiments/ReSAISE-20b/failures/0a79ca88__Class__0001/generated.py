import hmac
import hashlib
import random
from typing import Optional, Dict

# Global mapping of user IDs to their trusted cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted user IDs and signatures here.
}

# Simulated remote service that returns a user profile.
def _fetch_remote_profile(u_id: str) -> Dict[str, str]:
    """
    Simulates fetching a user profile from a remote service.
    Raises ConnectionError to mimic network failures.
    """
    # Simulate a 10% chance of connection failure.
    if random.random() < 0.1:
        raise ConnectionError(f"Unable to reach remote service for user '{u_id}'.")
    
    # In a real implementation, this would be an HTTP request.
    # Here we return a simple profile dictionary.
    return {"user_id": u_id, "name": f"User {u_id}", "email": f"{u_id}@example.com"}

def get_user_details(u_id: str, sig_code: str) -> Optional[Dict[str, str]]:
    """
    Retrieve a user profile from a remote service and verify its authenticity.

    Args:
        u_id: The unique identifier for the user whose profile is being fetched.
        sig_code: The cryptographic signature associated with the user profile.

    Returns:
        The user profile dictionary if the provided signature matches the trusted
        signature; otherwise, None.

    Raises:
        ConnectionError: If the remote service cannot be reached.
    """
    # Step 1: Validate that we have a trusted signature for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if expected_sig is None:
        # Unknown user – cannot trust any signature.
        return None

    # Step 2: Use constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(sig_code, expected_sig):
        # Signature does not match; reject the profile.
        return None

    # Step 3: Fetch the profile from the remote service.
    profile = _fetch_remote_profile(u_id)

    # The signature was already validated against the trusted value,
    # so we can safely return the profile.
    return profile