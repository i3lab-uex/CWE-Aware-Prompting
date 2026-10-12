# -*- coding: utf-8 -*-

"""
Utility to verify the authenticity of messages received from an external API.
"""

# Predefined dictionary containing correct signatures for each message ID.
# In a real application, this would be securely populated from a trusted source.
VALID_API_MESSAGES = {
    # Example entries:
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "0123456789abcdef1234",
    # Add more message IDs and their corresponding signatures here.
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message identifier.

    Parameters:
        msg_identifier (str): The ID of the message to validate.
        crypto_sign (str):   The cryptographic signature received.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Ensure the identifier exists; let KeyError propagate if not found.
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Perform a constant‑time comparison to mitigate timing attacks.
    # The built‑in `hmac.compare_digest` is suitable for this purpose.
    import hmac
    return hmac.compare_digest(expected_sign, crypto_sign)