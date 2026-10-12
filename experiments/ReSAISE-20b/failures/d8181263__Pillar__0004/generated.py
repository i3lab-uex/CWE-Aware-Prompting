import hashlib
import hmac

# Define a secret key that will be used for signing.
# In practice, this should be securely stored and not hard‑coded.
SECRET_KEY: bytes = b'super_secret_key_1234567890'

# Allowed cryptographic hash algorithms (secure only).
SECURE_ALGORITHMS = {
    'sha224', 'sha256', 'sha384', 'sha512',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
    'blake2b', 'blake2s',
    # SM3 is considered secure in Chinese standards
    'sm3'
}

def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified
    cryptographic hash algorithm.

    Parameters:
        algorithm (str): The name of the hashing algorithm to use.
        message   (bytes): The raw data that needs to be signed.

    Returns:
        bytes: The generated HMAC signature.

    Raises:
        ValueError: If an unsupported or insecure hash algorithm is specified.
    """
    # Normalise the algorithm name (case‑insensitive).
    algo = algorithm.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm}")

    # Ensure the algorithm is available in hashlib.
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm {algorithm} is not available on this system")

    # Create a new HMAC object with the chosen hash function.
    h = hmac.new(SECRET_KEY, message, hashlib.new(algo))

    return h.digest()