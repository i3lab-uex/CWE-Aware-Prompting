import hashlib
import hmac

# Secure hash algorithms suitable for HMAC.  Exclude weak or deprecated ones.
SECURE_HASHES = {
    'sha512_256', 'sha224', 'sha384',
    'blake2b', 'sha3_256', 'sha256',
    'sm3', 'sha3_224', 'shake_128',
    'sha512', 'sha512_224', 'shake_256',
    'sha3_512', 'blake2s', 'sha3_384'
}

# The secret key used for HMAC signing.  In real code this should be stored securely.
SECRET_KEY = b'super_secret_key_please_change'

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given data using the specified hash algorithm.

    Args:
        hash_algorithm (str): Desired hash algorithm name.
        content (bytes): Data to be signed.

    Returns:
        bytes: The HMAC signature.

    Raises:
        ValueError: If the specified hash algorithm is not supported or insecure.
    """
    # Normalize algorithm name
    alg = hash_algorithm.lower()
    if alg not in SECURE_HASHES:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm}")

    # Create a new HMAC object using the selected hash function
    h = hmac.new(SECRET_KEY, digestmod=hashlib.new)
    # The hashlib.new function requires the algorithm name as bytes
    h.update(content)
    return h.digest()