import hashlib
import hmac

# A secret key used for HMAC signing.
# In a real application this must be kept confidential and
# generated with sufficient entropy (e.g., os.urandom(32)).
SECRET_KEY: bytes = b'\x01\x23\x45\x67\x89\xab\xcd\xef' * 4

# Set of cryptographically secure hash algorithms that are
# considered safe for HMAC usage.  Insecure or legacy algorithms
# (e.g., md5, sha1) are deliberately omitted.
SECURE_HASH_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha512_224',
    'sha512_256',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
}

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given payload using
    the specified hash algorithm.

    Parameters:
        hash_algorithm_name (str): Name of the desired hash algorithm.
        payload (bytes): Data to be signed.

    Returns:
        bytes: HMAC signature of the payload.

    Raises:
        ValueError: If the hash algorithm is not supported or considered insecure.
    """
    # Normalise name to lower case and strip whitespace
    algo = hash_algorithm_name.strip().lower()

    # Verify that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algorithm_name}' is not available.")

    # Enforce use of only secure algorithms
    if algo not in SECURE_HASH_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{hash_algorithm_name}' is not considered secure for HMAC usage.")

    # Create a new HMAC object using the selected algorithm
    hmac_obj = hmac.new(SECRET_KEY, msg=payload, digestmod=algo)

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()