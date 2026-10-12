import hashlib
import hmac

# Secure hash algorithms that are considered safe for HMAC usage.
SECURE_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
    'sha512_224',
    'sha512_256',
}

# The secret key used for HMAC signing. In a real application this should
# be securely generated and stored (e.g., using os.urandom or a key
# management system). For demonstration purposes we use a static key.
secret_key = b'super-secret-key-please-change'

def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the provided message using the
    specified hash algorithm.

    Parameters:
        algorithm_name (str): The name of the hash algorithm to use.
        message (bytes): The data to be signed.

    Returns:
        bytes: The HMAC signature of the message.

    Raises:
        ValueError: If the algorithm is not supported or considered insecure.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Retrieve the hashlib constructor for the chosen algorithm
    try:
        hash_func = getattr(hashlib, algo)
    except AttributeError:
        raise ValueError(f"Hash algorithm {algorithm_name} is not available in hashlib")

    # Compute HMAC using the chosen hash function
    hmac_obj = hmac.new(secret_key, message, digestmod=hash_func)
    return hmac_obj.digest()