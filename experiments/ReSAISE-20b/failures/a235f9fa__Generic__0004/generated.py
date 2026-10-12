import hmac

# Example global dictionary of valid signatures for messages.
# In a real application this would be populated securely from
# a trusted source or configuration file.
VALID_API_MESSAGES = {
    # 'msg_id': 'signature',
    "12345": "a1b2c3d4e5f6g7h8i9j0",
    "67890": "z9y8x7w6v5u4t3s2r1q0",
    # Add more message IDs and their expected signatures here.
}


def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the cryptographic signature for a given message ID.

    Parameters
    ----------
    msg_id : str
        The identifier of the message to validate.
    sig : str
        The cryptographic signature provided by the external API.

    Returns
    -------
    bool
        True if the signature matches the stored valid signature for the given
        message ID; False otherwise.

    Raises
    ------
    KeyError
        If the `msg_id` is not present in the global VALID_API_MESSAGES
        dictionary.
    """
    # Retrieve the expected signature.  A KeyError will propagate if msg_id
    # is missing, as required.
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(sig, expected_sig)