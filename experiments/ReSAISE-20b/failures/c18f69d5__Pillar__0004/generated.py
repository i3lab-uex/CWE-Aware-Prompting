import hmac

# Global dictionary mapping message IDs to their expected cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries; replace with actual data in production
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "0j9i8h7g6f5e4d3c2b1a",
    # ... add more entries as needed
}

def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected value
    for a given API message ID.

    Parameters:
        api_message_id (str): Identifier of the API message.
        cryptographic_sign (str): Signature supplied by the external API.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If api_message_id is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if ID is missing
    try:
        expected_sign = VALID_API_MESSAGES[api_message_id]
    except KeyError as exc:
        raise KeyError(f"Message ID '{api_message_id}' not found in VALID_API_MESSAGES.") from exc

    # Use constant‑time comparison to mitigate timing attacks (CWE‑693)
    return hmac.compare_digest(expected_sign, cryptographic_sign)