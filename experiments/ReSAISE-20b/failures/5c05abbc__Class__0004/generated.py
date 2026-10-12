import hmac

# Predefined dictionary containing the correct signatures for API messages.
# Example structure: {"msg1": "signature_hex_string", ...}
VALID_API_MESSAGES = {
    # Populate with actual message IDs and their corresponding signatures.
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message ID.

    Parameters:
        msg_id (str): The unique identifier of the API message.
        sign  (str): The cryptographic signature supplied with the message.

    Returns:
        bool: True if the signature matches the stored value, False otherwise.

    Raises:
        KeyError: If msg_id is not present in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; let KeyError propagate if not found.
    stored_sign = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(stored_sign, sign)