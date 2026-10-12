import hashlib
import hmac

# Secret key used for HMAC signing (should be securely generated and stored)
secret_key: bytes = b"your-very-secure-secret-key"

# Whitelist of cryptographically strong hash algorithms supported by hashlib
_SECURE_ALGORITHMS = {
    "sha224",
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
    Create an HMAC signature using a secure hash algorithm.

    Args:
        algorithm_name: Name of the hash algorithm to use.
        payload: The raw data that will be signed.

    Returns:
        bytes: The computed HMAC signature.

    Raises:
        ValueError: If the algorithm is not supported or insecure.
    """
    # Normalise algorithm name to lowercase
    algo = algorithm_name.lower()

    if algo not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm_name}"
        )

    # Create the HMAC object using the chosen hash function
    h = hmac.new(secret_key, payload, getattr(hashlib, algo))
    return h.digest()