import hmac

# Example dictionary mapping API messages to their expected cryptographic signatures.
# In practice, this would be securely stored and managed.
VALID_API_MESSAGES = {
    "msg1": "a3f5c2d9e8b4... (example signature)",
    "msg2": "b7c1d3e9f0a2... (example signature)",
    # Add more messages as needed
}

def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    expected signature for a given API message.

    Parameters:
        api_message (str): The unique identifier of the API message.
        sig (str): The cryptographic signature to validate.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `api_message` does not exist in VALID_API_MESSAGES.
    """
    # Ensure the message exists; let KeyError propagate if not found
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)