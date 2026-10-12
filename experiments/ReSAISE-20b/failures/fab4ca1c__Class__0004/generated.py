import hmac

# Global dictionary mapping message identifiers to their valid signatures.
# In practice, this should be securely loaded from a trusted source.
VALID_API_MESSAGES = {
    # Example entries (signature strings are placeholders)
    "msg1": "a3f5c9d8e7b6...1234567890abcdef",
    "msg2": "b4d6e8f9a1c3...fedcba0987654321",
    # Add more entries as needed
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided signature matches the stored signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        The unique identifier of the API message.
    sign : str
        The cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` does not exist in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature; raise KeyError if not found
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use hmac.compare_digest for constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected_sign)