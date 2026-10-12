import hmac

# Global dictionary mapping message identifiers to their valid signatures.
# Example structure:
# VALID_API_MESSAGES = {
#     "msg123": b"base64encodedsignature==",
#     ...
# }
VALID_API_MESSAGES = {}  # This should be populated elsewhere in the application.

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Args:
        msg_identifier (str): Identifier of the message to verify.
        sign (str): The signature received from the external API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `msg_identifier` does not exist in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature for the message identifier.
    try:
        expected_sign = VALID_API_MESSAGES[msg_identifier]
    except KeyError as exc:
        # Re-raise with a clearer message
        raise KeyError(f"Message identifier '{msg_identifier}' not found.") from exc

    # Ensure both signatures are bytes for a secure comparison.
    if isinstance(sign, str):
        sign_bytes = sign.encode('utf-8')
    else:
        sign_bytes = sign

    if isinstance(expected_sign, str):
        expected_bytes = expected_sign.encode('utf-8')
    else:
        expected_bytes = expected_sign

    # Use hmac.compare_digest to avoid timing attacks.
    return hmac.compare_digest(sign_bytes, expected_bytes)