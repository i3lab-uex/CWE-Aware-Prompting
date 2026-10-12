import hashlib
import hmac

# Secret key used for HMAC signing (must be kept secret and not hard‑coded in production)
# In real applications this should come from a secure key store or environment variable.
secret_key = b"your-very-secret-key"

# Whitelist of secure hash algorithms suitable for HMAC
SECURE_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sm3",            # if supported by the platform
    "sha3_224",
    "shake_128",      # SHAKE functions are keyed but not standard for HMAC; included for completeness
    "sha512",
    "sha512_224",
    "shake_256",
    "sha3_512",
    "blake2s",
    "sha3_384",
}

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the desired hash algorithm (e.g., 'sha256').
    content : bytes
        The data to be signed.

    Returns
    -------
    bytes
        HMAC signature of the content.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or considered insecure.
    """
    # Normalise the algorithm name to lower case for comparison
    algo = hash_algorithm.lower()

    # Verify that the requested algorithm is both available and secure
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm}")

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is not available in the current Python environment")

    # Compute HMAC
    return hmac.new(secret_key, content, digestmod=algo).digest()