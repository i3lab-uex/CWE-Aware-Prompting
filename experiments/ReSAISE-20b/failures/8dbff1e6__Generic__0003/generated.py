import hashlib
import hmac

# A secure secret key for HMAC signing. In a real application this should be stored securely.
SECRET_KEY = b"super_secret_key_please_change"

# Algorithms that are considered insecure for cryptographic signatures
_INSECURE_ALGORITHMS = {
    "md5",
    "sha1",
    "ripemd160",  # not recommended for new protocols
}

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given payload using the specified hash algorithm.

    Args:
        hash_algorithm_name: Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
        payload: The data to be signed.

    Returns:
        A bytes object containing the HMAC signature.

    Raises:
        ValueError: If the hash algorithm is not supported or is insecure.
    """
    # Validate that the requested algorithm exists in hashlib
    if hash_algorithm_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm_name}")

    # Reject insecure algorithms
    if hash_algorithm_name.lower() in _INSECURE_ALGORITHMS:
        raise ValueError(f"Insecure hash algorithm not allowed: {hash_algorithm_name}")

    # Create the HMAC object with the chosen algorithm
    hmac_obj = hmac.new(SECRET_KEY, payload, getattr(hashlib, hash_algorithm_name.lower()))
    return hmac_obj.digest()