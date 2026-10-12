import hashlib
import hmac

def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC signature for the given payload using the specified hash algorithm.

    Args:
        hash_algorithm (str): Name of the hash function to use (e.g., 'sha256', 'blake2b').
        payload (bytes): The data to be signed.
        secret (bytes): The secret key used for signing.

    Returns:
        bytes: The computed HMAC signature.

    Raises:
        ValueError: If the requested hash algorithm is not supported by hashlib.
    """
    # Normalise algorithm name (hashlib uses lowercase names)
    algo = hash_algorithm.lower()

    # Verify that the algorithm is available
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create the HMAC object using the specified hash function
    h = hmac.new(secret, payload, digestmod=hashlib.new(algo))
    return h.digest()