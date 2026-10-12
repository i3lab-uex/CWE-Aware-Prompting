import hashlib
import hmac

# A secret key used for HMAC signing (should be kept confidential)
SECRET_KEY = b"your-very-secure-secret-key"

# Whitelist of secure hash algorithms
_SECURE_ALGORITHMS = {
    "sha256",
    "sha384",
    "sha512",
    "blake2b",
    "blake2s",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
}

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for the provided data using a secure hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Desired hash algorithm name (e.g., 'sha256', 'blake2b').
    content : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the content.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or considered insecure.
    """
    # Normalize and validate the algorithm name
    algo = hash_algorithm.lower()
    if algo not in _SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm}")

    # Create the HMAC object using the chosen hash function
    try:
        hmac_obj = hmac.new(SECRET_KEY, msg=content, digestmod=getattr(hashlib, algo))
    except AttributeError:
        # In case hashlib does not expose the algorithm (unlikely for whitelisted ones)
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is not available in hashlib")

    return hmac_obj.digest()