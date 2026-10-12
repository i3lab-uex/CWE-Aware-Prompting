import hashlib
import hmac

# Replace this with your actual secret key (bytes)
SECRET_KEY = b"your-very-secret-key"

# Set of hash algorithms considered secure for HMAC usage
SECURE_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sm3",
    "sha3_224",
    "shake_128",
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

    Args:
        algorithm_name: Name of the hash algorithm to use.
        message: Data to be signed (bytes).

    Returns:
        The HMAC signature as bytes.

    Raises:
        ValueError: If the algorithm is not supported or considered insecure.
    """
    # Normalize algorithm name
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Ensure the algorithm is available in hashlib
    try:
        hash_func = hashlib.new(algo)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm {algorithm_name} is not available in this environment") from exc

    # Create HMAC using the selected hash function
    hmac_obj = hmac.new(SECRET_KEY, message, digestmod=hash_func)
    return hmac_obj.digest()