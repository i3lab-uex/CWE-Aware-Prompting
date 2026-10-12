import hmac
from typing import Optional, Dict

# Global dictionary mapping user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted profiles here
}

def _fetch_remote_profile(u_id: str) -> Dict[str, str]:
    """
    Simulate fetching a user profile from a remote service.

    In a real implementation this would perform an HTTP request or similar.
    For demonstration purposes, we simply return a dictionary containing
    the user ID and an example profile data.
    """
    # Simulate network failure for unknown users
    if u_id not in TRUSTED_USER_PROFILES:
        raise ConnectionError(f"Unable to fetch profile for user {u_id}")

    # Example of a remote profile payload
    return {
        "user_id": u_id,
        "name": u_id.capitalize(),
        "email": f"{u_id}@example.com",
    }

def _constant_time_compare(a: str, b: str) -> bool:
    """
    Perform a constant‑time comparison of two strings to mitigate timing attacks.
    """
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))

def get_user_details(u_id: str, sig_code: str) -> Optional[Dict[str, str]]:
    """
    Retrieve a user profile from a remote service and validate its cryptographic
    signature against the trusted signatures list.

    Parameters:
        u_id (str): The unique identifier of the user.
        sig_code (str): The cryptographic signature provided with the profile.

    Returns:
        dict: The user profile if the signature is valid.
        None: If the signature does not match the expected value.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # Step 1: Fetch the user profile
    try:
        profile = _fetch_remote_profile(u_id)
    except ConnectionError as exc:
        # Re‑raise to adhere to the specified exception contract
        raise

    # Step 2: Retrieve expected signature from trusted list
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if expected_sig is None:
        # No trusted signature for this user; treat as invalid
        return None

    # Step 3: Verify the signature using constant‑time comparison
    if not _constant_time_compare(sig_code, expected_sig):
        return None

    # Signature is valid; return the fetched profile
    return profile