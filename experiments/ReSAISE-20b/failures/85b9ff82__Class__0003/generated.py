import hashlib
import hmac

# The secret key used for HMAC signing (must be kept confidential)
SECRET_KEY = b"your-very-secret-key"

# Whitelist of secure hash algorithms
ALLOWED_HASH_ALGORITHMS = {
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

def sign_message(hash_algorithm: str, content: bytes) -> bytes:
    """
    Create an HMAC signature for the given content using the specified hash algorithm.

    Args:
        hash_algorithm: Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
        content: Raw input data to be signed.

    Returns:
        The HMAC signature as bytes.

    Raises:
        ValueError: If the hash algorithm is unsupported or disallowed.
    """
    # Normalise and validate the hash algorithm name
    algo_name = hash_algorithm.lower()
    if algo_name not in ALLOWED_HASH_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {hash_algorithm}")

    # Create the HMAC object with the chosen hash function
    hmac_obj = hmac.new(SECRET_KEY, content, getattr(hashlib, algo_name))
    return hmac_obj.digest()