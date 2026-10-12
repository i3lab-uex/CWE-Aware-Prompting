import hashlib
import hmac

# Secret key used for HMAC generation (must be kept confidential)
secret_key: bytes = b"super_secret_key"

# Whitelist of secure hash algorithms supported by the function
SECURE_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "sha512",
    "sha3_384",
    "shake_128",
    "sha256",
    "blake2b",
    "shake_256",
    "sha3_256",
    "blake2s",
    "sha3_512",
    "sha3_224",
}

def create_checksum(algorithm_name: str, message_data: bytes) -> bytes:
    """
    Generate a cryptographic signature (HMAC) for the given data using
    a secure hash algorithm.

    Parameters:
        algorithm_name (str): Name of the hashing algorithm to use.
        message_data  (bytes): Raw data that needs to be signed.

    Returns:
        bytes: The generated HMAC signature.

    Raises:
        ValueError: If an unsupported or insecure hash algorithm is specified.
    """
    # Normalise the algorithm name to lower case
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm_name}"
        )

    # Create the HMAC object using the selected digest
    h = hmac.new(secret_key, message_data, digestmod=algo)
    return h.digest()