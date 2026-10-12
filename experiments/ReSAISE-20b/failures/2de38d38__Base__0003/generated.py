import hmac

# Global dictionary mapping message identifiers to their expected signatures.
VALID_API_MESSAGES = {
    # Example entries (replace with real values in production)
    "msg_001": "a3f5c8e1d2b4...",
    "msg_002": "7e9d3a6f0c1b...",
    # Add more message codes and their corresponding valid signatures here.
}


def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message code.

    Parameters:
        msg_code (str): Identifier of the API message.
        crypto_sign (str): Signature supplied by the external API.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If msg_code is not present in VALID_API_MESSAGES.
    """
    # Ensure the message code exists; let KeyError propagate if not found
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)