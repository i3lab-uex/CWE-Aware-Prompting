import hashlib
import hmac

# A secret key used for HMAC. In a real application this should be securely generated
# and stored (e.g., in an environment variable or a secrets manager).
SECRET_KEY = b"super-secret-key-that-is-very-long-and-random"

# Define a whitelist of cryptographic hash algorithms that are considered secure.
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
    Compute an HMAC signature of `content` using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        The name of a hash algorithm supported by hashlib (e.g. "sha256").
    content : bytes
        The raw data to sign.

    Returns
    -------
    bytes
        The HMAC digest of the content.

    Raises
    ------
    ValueError
        If `hash_algorithm` is not in the whitelist of allowed algorithms.
    """
    # Normalise algorithm name (hashlib uses lowercase names)
    algo_name = hash_algorithm.lower()

    if algo_name not in ALLOWED_HASH_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {hash_algorithm}"
        )

    # Create the HMAC object with the chosen hash function
    hmac_obj = hmac.new(SECRET_KEY, content, getattr(hashlib, algo_name))
    return hmac_obj.digest()