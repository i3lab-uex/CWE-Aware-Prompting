import random
from typing import Dict, Optional

# Global dictionary mapping user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user1": "sig123",
    "user2": "sig456",
    # Add more trusted user IDs and signatures as needed.
}

def _fetch_remote_profile(uid: str) -> Dict:
    """
    Simulates fetching a user profile from a remote service.
    
    In a real implementation this function would perform an HTTP request or
    another form of network communication. For demonstration purposes, it
    randomly raises a ConnectionError to mimic intermittent connectivity.
    
    Parameters:
        uid (str): The unique identifier of the user.
        
    Returns:
        dict: A dictionary representing the user's profile data.
    
    Raises:
        ConnectionError: If the remote service is unreachable.
    """
    # Simulate a 20% chance of network failure
    if random.random() < 0.2:
        raise ConnectionError(f"Failed to connect to remote service for UID {uid}")

    # Simulated user profiles (would normally come from a database or API)
    simulated_profiles = {
        "user1": {"uid": "user1", "name": "Alice Smith", "email": "alice@example.com"},
        "user2": {"uid": "user2", "name": "Bob Jones", "email": "bob@example.com"},
    }
    
    if uid not in simulated_profiles:
        raise ValueError(f"Profile for UID {uid} does not exist")

    return simulated_profiles[uid]


def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict]:
    """
    Retrieves a user profile from a remote service and validates its cryptographic signature.
    
    Parameters:
        uid (str): The unique identifier for the user whose profile is being fetched.
        sig (str): The cryptographic signature associated with the user profile.
    
    Returns:
        dict | None: The user profile dictionary if the signature is valid, otherwise None.
    
    Raises:
        ConnectionError: If it's not possible to fetch the profile from the remote service.
        ValueError: If the UID does not exist in the simulated data (used only for demonstration).
    """
    # First, check that we have a trusted signature for this UID
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # Unknown UID – treat as untrusted
        return None

    if sig != expected_sig:
        # Signature does not match – do not trust the profile
        return None

    # Attempt to fetch the profile from the remote service
    try:
        profile = _fetch_remote_profile(uid)
    except ConnectionError as e:
        # Propagate the connection error to the caller
        raise

    # Additional security checks could be performed here (e.g., schema validation).

    return profile