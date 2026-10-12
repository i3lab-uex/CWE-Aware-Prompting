import hashlib
import hmac

# A secret key used for signing. In a real application this should be stored
# securely (e.g., in an environment variable or a secrets manager).
SECRET_KEY = b"super-secret-key"

# A set of hash algorithms considered secure for HMAC usage.
SECURE_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha512_256",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash
    algorithm.

    Parameters:
        algorithm (str): Name of the hashing algorithm to use.
        message (bytes): Raw data that needs to be signed.

    Returns:
        bytes: The generated HMAC signature.

    Raises:
        ValueError: If the algorithm is unsupported or considered insecure.
    """
    algo = algorithm.lower()
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm!r}. "
            "Allowed algorithms are: " + ", ".join(sorted(SECURE_ALGORITHMS))
        )

    # Retrieve the constructor for the chosen algorithm from hashlib.
    try:
        hash_constructor = getattr(hashlib, algo)
    except AttributeError:
        # This should not happen because we validated the algorithm name.
        raise ValueError(f"Hash algorithm {algorithm!r} is not available in hashlib.")

    # Create the HMAC object and compute the digest.
    hmac_obj = hmac.new(SECRET_KEY, message, hash_constructor)
    return hmac_obj.digest()