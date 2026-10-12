import hashlib
import hmac

# Secret key used for HMAC. In a real application this should be stored securely.
secret_key: bytes = b"super_secret_hmac_key"

# List of cryptographically secure hash algorithms that are allowed.
ALLOWED_HASHES = {
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
    Create an HMAC signature of the given content using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    content : bytes
        The raw data to sign.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not in the list of allowed algorithms.
    """
    # Normalise algorithm name to lowercase for comparison
    algo = hash_algorithm.lower()
    if algo not in ALLOWED_HASHES:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {hash_algorithm}")

    # Create a new HMAC object using the chosen algorithm
    hmac_obj = hmac.new(secret_key, digestmod=hashlib.new(algo))
    hmac_obj.update(content)
    return hmac_obj.digest()