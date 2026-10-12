import hmac

# Example global dictionary of expected signatures.
# In a real application this would be populated securely.
VALID_API_MESSAGES = {
    "msg1": "a3f5e2c7b8d9e0f123456789abcdef01",
    "msg2": "4c6b7d8e9f0a1b2c3d4e5f67890abcdef",
    # ... other message IDs and their signatures
}

def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        The unique identifier for the API message to be verified.
    crypto_signature : str
        The cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    KeyError
        If `api_message_id` is not present in the global VALID_API_MESSAGES dict.
    """
    # Retrieve the expected signature; raise KeyError if not found
    try:
        expected_signature = VALID_API_MESSAGES[api_message_id]
    except KeyError as exc:
        raise KeyError(f"API message ID '{api_message_id}' not found.") from exc

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)