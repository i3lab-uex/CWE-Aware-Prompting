import hmac
from typing import Dict

# Example dictionary of valid signatures for API messages.
# In a real application, this would be populated from secure storage
# and never hard‑coded. It is kept global to satisfy the specification.
VALID_API_MESSAGES: Dict[str, str] = {
    # msg_identifier : expected_cryptographic_signature
    "msg-001": "a1b2c3d4e5f67890abcdef1234567890",
    "msg-002": "0987654321fedcba0f1e2d3c4b5a6978",
    # Add more entries as needed
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Validate the cryptographic signature of a message from an external API.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier for the message being checked.
    crypto_signature : str
        Cryptographic signature provided by the external API.

    Returns
    -------
    bool
        True if the signature matches the stored value for the given identifier,
        False otherwise.

    Raises
    ------
    KeyError
        If ``msg_identifier`` does not exist in the VALID_API_MESSAGES dictionary.
    """
    # Ensure the message identifier exists; raise KeyError if not
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Message identifier '{msg_identifier}' is unknown.")

    # Retrieve the expected signature
    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)