import hashlib
import hmac

# List of cryptographic hash algorithms that are considered secure
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
    "sm3",          # SM3 is considered secure in many jurisdictions
}

# Secret key used for HMAC; in a real application this should be stored securely
SECRET_KEY = b"your-very-secure-secret-key"

def create_checksum(algorithm_name: str, message_data: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given data using the specified
    hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hashing algorithm to use.
    message_data : bytes
        Raw data that needs to be signed.

    Returns
    -------
    bytes
        The generated HMAC signature.

    Raises
    ------
    ValueError
        If an unsupported or insecure hash algorithm is specified.
    """
    # Normalise the algorithm name (hashlib expects lowercase)
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure algorithm '{algorithm_name}'. "
            f"Supported algorithms: {', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Create an HMAC object with the chosen hash algorithm
    hmac_obj = hmac.new(SECRET_KEY, message_data, digestmod=algo)

    # Return the raw bytes of the HMAC
    return hmac_obj.digest()