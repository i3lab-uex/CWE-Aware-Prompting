import hashlib
import hmac

# Secret key used for HMAC signing (must be kept confidential in real deployments)
SECRET_KEY: bytes = b"your-very-secret-key"

# Define a whitelist of hash algorithms considered secure for HMAC usage.
ALLOWED_HASHES = {
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Create an HMAC signature for the given payload using a specified hash algorithm.

    Args:
        algorithm_name: Name of the hash algorithm to use (must be in ALLOWED_HASHES).
        payload: Raw data bytes to sign.

    Returns:
        The HMAC signature as a byte string.

    Raises:
        ValueError: If the requested algorithm is not in the whitelist.
    """
    # Normalize algorithm name to lowercase for comparison
    algo = algorithm_name.lower()

    if algo not in ALLOWED_HASHES:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {algorithm_name!r}. "
            f"Allowed algorithms are: {sorted(ALLOWED_HASHES)}"
        )

    # Verify that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm {algorithm_name!r} is not available on this system.")

    # Compute the HMAC signature
    return hmac.new(SECRET_KEY, payload, digestmod=algo).digest()