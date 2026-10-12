import hashlib
import hmac

# Define a secret key (in practice this should be stored securely)
secret_key: bytes = b"super_secret_key_please_change"

# Whitelist of secure hash algorithms supported by hashlib
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
    # SHA-512/256 and SHA-512/224 are also considered secure
    "sha512_256",
}

def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given message using
    the specified secure hash algorithm.

    Parameters:
        algorithm (str): Name of the hashing algorithm to use.
        message (bytes): Raw data that needs to be signed.

    Returns:
        bytes: The generated HMAC signature.

    Raises:
        ValueError: If an unsupported or insecure hash algorithm is specified.
    """
    # Normalise the algorithm name to lower case
    algo = algorithm.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure algorithm '{algorithm}'. "
            "Supported algorithms are: "
            f"{', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Create a new HMAC object using the chosen algorithm
    h = hmac.new(secret_key, digestmod=algo)
    h.update(message)

    return h.digest()