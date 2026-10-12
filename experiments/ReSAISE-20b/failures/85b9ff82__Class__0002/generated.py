import hashlib
import hmac

# Secure hash algorithms that are considered safe for HMAC usage.
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

# Secret key used for HMAC. In a real system this should be stored securely.
SECRET_KEY = b"your-very-secure-secret-key"

def sign_message(hash_algorithm: str, content: bytes) -> bytes:
    """
    Create an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g., "sha256").
    content : bytes
        Raw data to sign.

    Returns
    -------
    bytes
        The HMAC digest of the content.

    Raises
    ------
    ValueError
        If the provided hash algorithm is not supported or disallowed.
    """
    # Normalise algorithm name to lower case for comparison
    algo = hash_algorithm.lower()

    if algo not in ALLOWED_HASHES:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {hash_algorithm}")

    # Create a new HMAC object with the chosen algorithm
    h = hmac.new(SECRET_KEY, digestmod=getattr(hashlib, algo))
    h.update(content)
    return h.digest()