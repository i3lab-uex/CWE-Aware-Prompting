import hmac

# Global dictionary mapping message identifiers to their correct cryptographic signatures.
VALID_API_MESSAGES = {
    "msg001": "a1b2c3d4e5f6g7h8i9j0",
    "msg002": "1234567890abcdef1234",
    # Add more message IDs and signatures as needed
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        The ID of the message whose authenticity needs to be verified.
    crypto_sign : str
        The cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the stored value; False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature; raise KeyError if not found
    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(crypto_sign, expected_signature)