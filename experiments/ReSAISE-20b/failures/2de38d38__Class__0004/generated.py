import hmac
from typing import Dict

# Example global dictionary of valid signatures for API messages.
# In a real application this would be securely stored and managed.
VALID_API_MESSAGES: Dict[str, str] = {
    # msg_code : hex-encoded signature
    "order_created": "5f2d3a7b9c4e1f0a8b6c2d4e5f3a7b9c",
    "payment_received": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p",
    # Add more message codes and their corresponding signatures as needed
}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the cryptographic signature provided for a message matches
    the expected signature stored in VALID_API_MESSAGES.

    Args:
        msg_code (str): Identifier of the message to validate.
        crypto_sign (str): Hex-encoded cryptographic signature from the API.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If msg_code is not present in VALID_API_MESSAGES.
    """
    # Ensure the message code exists
    if msg_code not in VALID_API_MESSAGES:
        raise KeyError(f"Message code '{msg_code}' is unknown")

    # Retrieve the expected signature
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Perform a constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)