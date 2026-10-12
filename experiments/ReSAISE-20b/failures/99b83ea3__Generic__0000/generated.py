import hashlib
import hmac

# Secret key used for HMAC signing (must be kept confidential).
# In a real application this should come from a secure source, e.g. environment variable or key vault.
secret_key: bytes = b"super_secret_key"

# Define a set of cryptographically secure hash algorithms.
SECURE_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sm3",          # SM3 is considered secure in Chinese cryptographic standards
    "sha3_224",
    "shake_128",    # SHAKE is an extendable-output function, considered secure
    "sha512",
    "sha512_224",
    "shake_256",
    "sha3_512",
    "blake2s",
    "sha3_384",
}

def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256').
    message : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or considered insecure.
    """
    # Normalise the algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm_name!r}. "
            f"Supported algorithms are: {sorted(SECURE_ALGORITHMS)}"
        )

    # Verify that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm {algorithm_name!r} is not available in this Python build.")

    # Compute the HMAC using the chosen algorithm
    signature = hmac.new(secret_key, message, digestmod=algo).digest()
    return signature