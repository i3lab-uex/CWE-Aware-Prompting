import hmac

# Example global dictionary containing valid signatures for API messages.
# In a real-world scenario this would be securely populated from a trusted source.
VALID_API_MESSAGES = {
    "msg001": "a1b2c3d4e5f6g7h8i9j0",
    "msg002": "b2c3d4e5f6g7h8i9j0k1",
    # Add more message IDs and their corresponding signatures here.
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message ID.

    Parameters
    ----------
    msg_id : str
        The identifier of the message whose authenticity is to be verified.
    sign : str
        The cryptographic signature supplied with the message.

    Returns
    -------
    bool
        True if the signatures match; False otherwise.

    Raises
    ------
    KeyError
        If `msg_id` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature; raise KeyError if not found
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use constant-time comparison to mitigate timing attacks (CWE-347)
    return hmac.compare_digest(sign, expected_sign)