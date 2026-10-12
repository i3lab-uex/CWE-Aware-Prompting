import hashlib
import hmac

# A secret key for HMAC; in a real system this should be securely generated
# and stored (e.g., environment variable, key management service).
SECRET_KEY = b"my_very_secret_key"

# Hash algorithms that are considered secure for HMAC usage.
ALLOWED_HASHES = {
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
    Create an HMAC signature of `content` using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    content : bytes
        The data to be signed.

    Returns
    -------
    bytes
        HMAC digest of the content.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not in the list of allowed algorithms.
    """
    # Normalise algorithm name to lower case
    algo = hash_algorithm.lower()

    if algo not in ALLOWED_HASHES:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {hash_algorithm}")

    # Construct the HMAC object with the chosen digest module
    h = hmac.new(SECRET_KEY, content, digestmod=algo)
    return h.digest()