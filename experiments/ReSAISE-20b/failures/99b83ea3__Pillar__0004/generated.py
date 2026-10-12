import hashlib
import hmac

# List of cryptographically secure hash algorithms supported by hashlib.
# Excludes weak algorithms such as md5 and sha1.
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
    "ripemd160",   # considered secure for many applications
}

# Key used in the HMAC signing procedure (should be kept secret).
# In a real application this key should come from a secure source.
SECRET_KEY = b"super_secret_key"

def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using a secure hash algorithm.

    Args:
        algorithm_name: Name of the desired hash algorithm.
        message: Data to be signed (bytes).

    Returns:
        HMAC signature as bytes.

    Raises:
        ValueError: If the specified algorithm is not supported or insecure.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Create a new HMAC object with the chosen algorithm
    try:
        hmac_obj = hmac.new(SECRET_KEY, message, digestmod=algo)
    except ValueError as e:
        # hashlib may raise ValueError if the algorithm name is invalid
        raise ValueError(f"Invalid hash algorithm: {algorithm_name}") from e

    return hmac_obj.digest()