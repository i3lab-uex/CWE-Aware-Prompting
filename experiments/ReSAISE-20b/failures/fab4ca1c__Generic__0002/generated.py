from typing import Dict

# Global dictionary containing valid signatures for API messages.
VALID_API_MESSAGES: Dict[str, str] = {
    # Example entries; replace with real data in production.
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # Add more message identifiers and their corresponding signatures here.
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters:
        msg_identifier (str): Identifier of the message to verify.
        sign (str): Cryptographic signature received from the external API.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError will propagate if missing.
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Constant‑time comparison to mitigate timing attacks.
    if len(sign) != len(expected_sign):
        return False

    # Compare each character without early exit.
    result = 0
    for a, b in zip(sign, expected_sign):
        result |= ord(a) ^ ord(b)

    return result == 0