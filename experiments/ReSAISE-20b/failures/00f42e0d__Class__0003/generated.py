import hashlib
import hmac

def sign_message(hash_name: str, message: bytes, key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Args:
        hash_name: Name of the hash algorithm (e.g. 'sha256', 'blake2b', etc.).
        message: The message to sign (bytes).
        key: The secret key used for signing (bytes).

    Returns:
        bytes: The HMAC digest of the message.

    Raises:
        ValueError: If the specified hash algorithm is not available.
    """
    # Validate that the hash algorithm exists in hashlib
    try:
        # This will raise a ValueError if hash_name is unsupported.
        _ = hashlib.new(hash_name)
    except (ValueError, TypeError):
        raise ValueError(f"Hash algorithm '{hash_name}' is not available")

    # Compute the HMAC using the chosen hash function
    hmac_obj = hmac.new(key, message, digestmod=hashlib)
    return hmac_obj.digest()