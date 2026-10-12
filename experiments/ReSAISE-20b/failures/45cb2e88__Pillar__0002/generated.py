import hashlib
import hmac

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for the given content using the specified hash algorithm.

    Args:
        algorithm (str): Name of the hash function to use (e.g., 'sha256', 'blake2b').
        content (bytes): The data to be signed.
        secret_key (bytes): The secret key used for HMAC.

    Returns:
        bytes: The computed HMAC signature.

    Raises:
        ValueError: If the specified algorithm is not supported by hashlib.
    """
    # Normalize algorithm name to lower case for lookup
    algo_name = algorithm.lower()

    # Verify that the requested algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm!r}")

    # Create HMAC object and compute the digest
    hmac_obj = hmac.new(secret_key, content, digestmod=algo_name)
    return hmac_obj.digest()