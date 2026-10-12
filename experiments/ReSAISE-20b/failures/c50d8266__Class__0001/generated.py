import hashlib
import hmac

# A secret key used for generating the HMAC signature.
# In a real application this should be stored securely (e.g., in an environment
# variable or a secrets manager) and not hard‑coded.
secret_key: bytes = b"super_secret_key"

# Set of hash algorithms considered secure for HMAC usage.
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
}

def create_checksum(algorithm_name: str, message_data: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given data using
    the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., "sha256").
    message_data : bytes
        The raw data that needs to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the data.

    Raises
    ------
    ValueError
        If an unsupported or insecure hash algorithm is specified.
    """
    # Normalise the algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm_name!r}. "
            "Allowed algorithms are: "
            f"{', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Create an HMAC object using the selected hash function
    h = hmac.new(secret_key, message_data, digestmod=algo)

    # Return the raw bytes of the HMAC digest
    return h.digest()