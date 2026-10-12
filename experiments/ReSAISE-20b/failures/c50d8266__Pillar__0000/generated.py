import hashlib
import hmac

# List of cryptographic hash algorithms considered secure for this context.
SECURE_ALGORITHMS = {
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
    "sm3",          # SM3 is considered secure in many standards
}

def create_checksum(algorithm_name: str, message_data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC-based cryptographic signature for the given data using
    a secure hash algorithm.

    Args:
        algorithm_name: Name of the hashing algorithm to use.
        message_data: Raw data that needs to be signed (bytes).
        secret_key: Secret key used for HMAC generation (bytes).

    Returns:
        The generated signature as bytes.

    Raises:
        ValueError: If the specified algorithm is unsupported or considered insecure.
    """
    # Normalise algorithm name (hashlib accepts lower‑case names)
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm_name!r}. "
            "Supported algorithms are: "
            f"{', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Create HMAC object with the chosen digest method
    h = hmac.new(secret_key, message_data, digestmod=algo)

    # Return the raw bytes of the HMAC
    return h.digest()