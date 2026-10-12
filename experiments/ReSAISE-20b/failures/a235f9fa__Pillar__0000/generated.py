import hmac

# NOTE: VALID_API_MESSAGES must be defined elsewhere in the application.
# It should map message IDs (str) to their expected cryptographic signatures (str).
# Example:
# VALID_API_MESSAGES = {
#     "msg_001": "a1b2c3d4e5f6...",
#     ...
# }

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters:
        msg_id (str): Identifier of the message to validate.
        sig   (str): Cryptographic signature supplied by the external API.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in the global VALID_API_MESSAGES
                  dictionary.
    """
    # Retrieve the expected signature; raise KeyError if msg_id is unknown
    try:
        expected_sig = VALID_API_MESSAGES[msg_id]
    except KeyError as exc:
        raise KeyError(f"Message ID '{msg_id}' not found in VALID_API_MESSAGES.") from exc

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)