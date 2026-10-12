import hashlib
import hmac

# Secret key used for HMAC signing (must be kept secret in production)
secret_key: bytes = b"your-very-secret-key"

# Set of secure hash algorithms supported by this function
SECURE_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sm3",          # SHA-3 variant (used in some standards)
    "sha3_224",
    "shake_128",    # variable-length output; use with a fixed digest size
    "sha512",
    "sha512_224",
    "shake_256",
    "sha3_512",
    "blake2s",
    "sha3_384",
}

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate an HMAC-based cryptographic signature for the given payload
    using the specified hash algorithm.

    Args:
        hash_algorithm_name: Name of the desired hash algorithm.
        payload: Data to be signed (bytes).

    Returns:
        The HMAC signature as bytes.

    Raises:
        ValueError: If the specified algorithm is not supported or insecure.
    """
    if hash_algorithm_name.lower() not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {hash_algorithm_name}"
        )

    # Obtain the hashlib constructor for the chosen algorithm
    try:
        hash_func = getattr(hashlib, hash_algorithm_name.lower())
    except AttributeError:
        raise ValueError(f"Hash algorithm not available in hashlib: {hash_algorithm_name}")

    # Create the HMAC object and compute the digest
    hmac_obj = hmac.new(secret_key, payload, digestmod=hash_func)
    return hmac_obj.digest()