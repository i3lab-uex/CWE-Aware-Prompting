import hmac

# Example predefined dictionary of valid signatures.
# In a real system this would be populated securely and not hard‑coded.
VALID_API_MESSAGES = {
    "msg_001": "a3f1c2d4e5b6...",
    "msg_002": "7b8a9c0d1e2f...",
    # ... other message IDs and their correct signatures
}

def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        The unique identifier of the API message.
    cryptographic_sign : str
        The signature supplied by the external API.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If `api_message_id` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature; KeyError propagates if ID is missing
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to mitigate timing attacks (CWE-347)
    return hmac.compare_digest(expected_sign, cryptographic_sign)