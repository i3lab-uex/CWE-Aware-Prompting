import hashlib
import hmac

# A global secret key used for signing.
# In a real application this should be stored securely (e.g., environment variable, key vault).
secret_key: bytes = b"your-very-secure-secret-key"

# Set of hash algorithms considered secure for HMAC usage.
SECURE_HASH_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha512_256",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    # sm3 is a Chinese standard; include if you trust it.
    "sm3",
}

def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for *message* using the specified *algorithm*.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        Raw data to be signed.

    Returns
    -------
    bytes
        The HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If *algorithm* is not in the list of supported secure algorithms or if it is unavailable.
    """
    # Normalise algorithm name to lower case
    algo = algorithm.lower()

    if algo not in SECURE_HASH_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm}")

    # Ensure the requested algorithm is actually available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm {algorithm} is not available on this system")

    # Create HMAC using the chosen hash function
    hmac_obj = hmac.new(secret_key, message, digestmod=algo)
    return hmac_obj.digest()