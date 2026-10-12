import hashlib
import hmac

# A globally available secret key used for signing.
# In a real application this should be stored securely (e.g. in a vault).
secret_key: bytes = b"your-very-secure-secret-key"

# Algorithms that are considered insecure for cryptographic signing.
INSECURE_ALGORITHMS = {
    "md5",
    "sha1",
    "md5-sha1",
}

# The set of algorithms supported by hashlib (lower‑case).
SUPPORTED_ALGORITHMS = {alg.lower() for alg in hashlib.algorithms_available}


def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given message using
    the specified hashing algorithm.

    Args:
        algorithm: Name of the hash algorithm (case‑insensitive).
        message: Raw data to be signed.

    Returns:
        The HMAC signature as bytes.

    Raises:
        ValueError: If the algorithm is unsupported or insecure.
    """
    if not isinstance(algorithm, str):
        raise TypeError("algorithm must be a string")

    alg = algorithm.lower()

    # Verify that the algorithm is available and secure
    if alg not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    if alg in INSECURE_ALGORITHMS:
        raise ValueError(f"Insecure hash algorithm not allowed: {algorithm}")

    # Create the HMAC signature
    try:
        h = hmac.new(secret_key, message, digestmod=alg)
    except ValueError as exc:
        # hmac.new raises ValueError if the digestmod is not a valid callable
        raise ValueError(f"Failed to create HMAC with algorithm '{algorithm}': {exc}") from exc

    return h.digest()