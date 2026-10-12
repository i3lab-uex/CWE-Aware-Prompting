import hmac
from typing import Dict

# Example global dictionary containing valid signatures for messages.
# In a real application this would be populated securely from a trusted source.
VALID_API_MESSAGES: Dict[str, str] = {
    # message_id : expected_signature
    "msg-001": "5f2c8a1b3d7e9f4c6a0b2e1d",
    "msg-002": "8a7f9c4e5b2d1a3f6e0c7b8d",
    # Add more entries as needed
}

def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided `signature` matches the expected cryptographic
    signature for the given `message_id`.

    Parameters
    ----------
    message_id : str
        The unique identifier of the message to be authenticated.
    signature : str
        The cryptographic signature provided by the external API.

    Returns
    -------
    bool
        True if the signature is valid for the message_id, False otherwise.

    Raises
    ------
    KeyError
        If `message_id` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve expected signature; raise KeyError if not found
    expected_sig = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(signature, expected_sig)