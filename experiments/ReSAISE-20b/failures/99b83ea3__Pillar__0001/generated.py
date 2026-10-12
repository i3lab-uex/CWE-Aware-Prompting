import hashlib
import hmac

# List of cryptographically strong hash algorithms supported by hashlib
_STRONG_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'blake2b',
    'sha3_256',
    'sha256',
    'sm3',          # SM3 is considered secure in its domain
    'sha3_224',
    'sha512',
    'sha512_224',
    'sha3_512',
    'blake2s',
    'sha3_384',
}

# The secret key used for HMAC. In a real application this should be
# securely stored and rotated as needed.
_SECRET_KEY = b'super_secret_key_change_me'


def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified
    hash algorithm.

    Args:
        algorithm_name: The name of the hash algorithm to use (e.g. 'sha256').
        message: The data to sign as bytes.

    Returns:
        A byte string containing the HMAC signature.

    Raises:
        ValueError: If the requested algorithm is not supported or is
                    considered weak.
    """
    # Normalize the algorithm name to lowercase for comparison
    algo = algorithm_name.lower()

    if algo not in _STRONG_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Ensure the algorithm exists in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not available in this Python environment")

    # Create an HMAC object using the selected hash function
    h = hmac.new(_SECRET_KEY, msg=message, digestmod=getattr(hashlib, algo))
    return h.digest()