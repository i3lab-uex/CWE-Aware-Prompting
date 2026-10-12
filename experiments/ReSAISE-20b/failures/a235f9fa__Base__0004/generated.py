import hmac

# Global dictionary mapping message IDs to their expected signatures.
# Signatures are stored as hex-encoded strings for readability.
VALID_API_MESSAGES = {
    # Example entries (replace with actual values)
    "msg_001": "a3f5c2d1e4b6f8... (hex signature)",
    "msg_002": "7c1d3e9b4a6f2... (hex signature)",
    # Add more message IDs and their corresponding signatures here.
}


def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the cryptographic signature of a message received from an external API.

    Parameters
    ----------
    msg_id : str
        The identifier for the message whose authenticity needs to be checked.
    sig : str
        The cryptographic signature associated with the specified message.  It is expected to be a hex-encoded string.

    Returns
    -------
    bool
        True if the provided signature matches the expected signature for ``msg_id``;
        otherwise False.

    Raises
    ------
    KeyError
        If ``msg_id`` does not exist in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature for the given message ID
    try:
        expected_sig_hex = VALID_API_MESSAGES[msg_id]
    except KeyError as exc:
        # Explicitly re-raise to satisfy the requirement
        raise KeyError(f"Message ID '{msg_id}' not found in VALID_API_MESSAGES.") from exc

    # Ensure the provided signature is a string; if not, raise TypeError
    if not isinstance(sig, str):
        raise TypeError("Signature must be a hex-encoded string.")

    # Convert both signatures to bytes for constant-time comparison
    try:
        expected_sig_bytes = bytes.fromhex(expected_sig_hex)
        provided_sig_bytes = bytes.fromhex(sig)
    except ValueError as exc:
        # Invalid hex string
        raise ValueError("Signature must be a valid hex-encoded string.") from exc

    # Use hmac.compare_digest for constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig_bytes, provided_sig_bytes)