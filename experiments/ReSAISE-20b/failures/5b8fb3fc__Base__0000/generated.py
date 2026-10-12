import json
import urllib.request
import urllib.error
from typing import Any, Dict, Optional
import hmac

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "a1b2c3d4e5f6g7h8i9j0",
    "bob":   "1234567890abcdef1234",
    # Add more trusted user signatures here.
}

def _fetch_remote_profile(uid: str) -> Dict[str, Any]:
    """
    Simulate a remote service call that returns a user profile in JSON format.
    In a real implementation, this would perform an HTTP request to the
    remote API endpoint.

    Raises:
        ConnectionError: If the remote service is unreachable or returns
                          a non-success HTTP status code.
    """
    # For demonstration purposes, we use a static URL pattern.
    url = f"https://example.com/api/users/{uid}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status != 200:
                raise ConnectionError(f"Unexpected HTTP status {response.status}")
            data = response.read()
            profile = json.loads(data.decode("utf-8"))
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to reach remote service: {e}") from e
    except json.JSONDecodeError as e:
        raise ConnectionError(f"Invalid JSON response for user {uid}") from e

    return profile


def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and validate its cryptographic
    signature against the trusted list.

    Parameters:
        uid (str): The unique identifier of the user.
        sig (str): The cryptographic signature provided with the profile.

    Returns:
        dict: The user profile if the signature matches the trusted value.
        None: If the signature does not match.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # Fetch the profile from the remote service.
    profile = _fetch_remote_profile(uid)

    # Retrieve the expected signature for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # No trusted signature known for this user; reject the profile.
        return None

    # Use constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # Signature verified; return the profile.
    return profile