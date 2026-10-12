import hashlib
import hmac

# A secret key used for the HMAC. In a real application this should be
# stored securely (e.g., in an environment variable or key‑management service).
SECRET_KEY = b'super_secret_key_please_change_me'

# Hash algorithms considered secure for HMAC usage
ALLOWED_HASHES = {
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

def sign_message(hash_algorithm: str, content: bytes) -> bytes:
    """
    Create an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    content : bytes
        The raw data to sign.

    Returns
    -------
    bytes
        The HMAC signature.

    Raises
    ------
    ValueError
        If the provided hash algorithm is unsupported or disallowed.
    """
    # Normalise to lower case for comparison
    algo = hash_algorithm.lower()

    if algo not in ALLOWED_HASHES:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {hash_algorithm}")

    # Retrieve the corresponding constructor from hashlib
    try:
        hasher = getattr(hashlib, algo)
    except AttributeError:
        # This should not happen because we validated against ALLOWED_HASHES
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is not available in hashlib")

    # Create the HMAC object using the chosen hash function
    h = hmac.new(SECRET_KEY, msg=content, digestmod=hasher)
    return h.digest()