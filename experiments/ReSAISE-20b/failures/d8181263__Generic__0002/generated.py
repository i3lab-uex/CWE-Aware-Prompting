import hashlib
import hmac

# Example secret key used for signing.
# In a real application this should be securely stored and managed.
secret_key: bytes = b'super_secret_key'

# A set of hash algorithms that are considered secure for signing purposes.
SECURE_ALGORITHMS = {
    'sha224', 'sha256', 'sha384', 'sha512',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
    'blake2b', 'blake2s',
    # sm3 is a Chinese standard hash algorithm that is still considered secure.
    'sm3',
}

def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate a cryptographic signature for `message` using HMAC with the
    specified hash algorithm.

    Parameters:
        algorithm (str): Name of the hashing algorithm to use.
        message (bytes): Raw data that needs to be signed.

    Returns:
        bytes: The HMAC signature of the message.

    Raises:
        ValueError: If an unsupported or insecure hash algorithm is specified.
    """
    # Normalize the algorithm name to lower case for comparison
    algo = algorithm.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm!r}. "
            f"Supported algorithms are: {sorted(SECURE_ALGORITHMS)}"
        )

    # Create a new HMAC object using the selected hash algorithm
    h = hmac.new(secret_key, message, algo)
    return h.digest()