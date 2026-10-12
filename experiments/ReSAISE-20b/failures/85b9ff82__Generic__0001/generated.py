import hashlib
import hmac

# Define a set of cryptographically secure hash algorithms.
# Exclude weak or non‑standard algorithms such as md5, sha1, ripemd160,
# and the variable‑length SHAKE functions.
_SECURE_HASH_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
}

# The secret key used for HMAC signing.
SECRET_KEY = b'\x01\x02\x03\x04'  # replace with your actual key

def sign_message(hash_algorithm: str, content: bytes) -> bytes:
    """
    Create an HMAC signature for the given content using the specified
    hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256').
    content : bytes
        Raw data that should be signed.

    Returns
    -------
    bytes
        The HMAC digest of the content.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or disallowed.
    """
    # Normalise the name to lowercase for comparison
    algo = hash_algorithm.lower()

    if algo not in _SECURE_HASH_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {hash_algorithm}")

    # Create the HMAC object using the chosen hash function
    hmac_obj = hmac.new(SECRET_KEY, content, digestmod=algo)
    return hmac_obj.digest()