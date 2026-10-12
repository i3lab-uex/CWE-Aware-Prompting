import hashlib
import hmac

def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC signature for the given payload using the specified hash algorithm.

    Args:
        hash_algorithm (str): Name of the hash function to use.
        payload (bytes): Data to be signed.
        secret (bytes): Secret key for HMAC.

    Returns:
        bytes: The computed HMAC signature.

    Raises:
        ValueError: If the requested hash algorithm is not supported.
    """
    # Ensure the hash algorithm is available in hashlib
    if hash_algorithm.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create a new hash constructor for the specified algorithm
    hash_constructor = hashlib.new(hash_algorithm)

    # Compute HMAC using the provided secret and payload
    hmac_obj = hmac.new(secret, payload, hash_constructor)
    return hmac_obj.digest()