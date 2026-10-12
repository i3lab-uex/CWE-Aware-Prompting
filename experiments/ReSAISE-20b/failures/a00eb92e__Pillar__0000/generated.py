import hmac
from typing import Dict

# Example global dictionary containing valid signatures for API messages.
# In a real application this would be populated securely from a trusted source.
VALID_API_MESSAGES: Dict[str, str] = {
    # msg_identifier : signature
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "abcdef1234567890fedcba",
    # Add more entries as needed.
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        The ID of the message to verify.
    crypto_sign : str
        The cryptographic signature provided with the message.

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if not found
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)