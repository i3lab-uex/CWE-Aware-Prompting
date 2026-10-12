import hashlib
import hmac

def generate_signature(hash_algo: str, input_data: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for the given data using the specified hash algorithm.

    Args:
        hash_algo: Name of the hash function to use (e.g., 'sha256', 'blake2b').
        input_data: Data to be signed (bytes).
        secret_key: Secret key for HMAC (bytes).

    Returns:
        The HMAC signature as bytes.

    Raises:
        ValueError: If the requested hash algorithm is not supported by hashlib.
    """
    # Normalise the algorithm name to lowercase for consistency
    algo = hash_algo.lower()

    # Ensure the requested algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo}")

    # Create the HMAC object and compute the digest
    return hmac.new(secret_key, input_data, algo).digest()