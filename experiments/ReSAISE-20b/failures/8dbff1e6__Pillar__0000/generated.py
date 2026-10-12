import hmac
import hashlib

# Secret key used for HMAC signing (must be kept confidential)
secret_key: bytes = b"your-very-secret-key"

# Set of cryptographically secure hash algorithms (Python 3.10+)
SECURE_HASH_ALGORITHMS = {
    "sha512_256",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sha512",
    "sha512_224",
    "sha3_512",
    "blake2s",
    "sha3_384",
}

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate an HMAC signature for the given payload using the specified hash algorithm.

    Args:
        hash_algorithm_name: The name of the desired hash algorithm (e.g., 'sha256').
        payload: Data to be signed.

    Returns:
        bytes: The HMAC signature.

    Raises:
        ValueError: If the specified algorithm is not supported or considered insecure.
    """
    # Normalise the hash name (case‑insensitive)
    algo = hash_algorithm_name.lower()

    if algo not in SECURE_HASH_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm_name}")

    # Create a new HMAC object using the chosen hash constructor
    hmac_obj = hmac.new(secret_key, payload, hashlib.new(algo))
    return hmac_obj.digest()