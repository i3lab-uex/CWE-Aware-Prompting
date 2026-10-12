import hashlib
import hmac

# Secret key used for HMAC signing (should be kept confidential)
SECRET_KEY: bytes = b"your-very-secure-secret-key"

# Algorithms that are considered insecure for cryptographic signing
INSECURE_ALGORITHMS = {
    "md5",
    "sha1",
    "sha224",  # considered weak for many contexts
    "md5-sha1",
}

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    content : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the content.

    Raises
    ------
    ValueError
        If the hash algorithm is not available or is considered insecure.
    """
    # Normalize algorithm name (hashlib uses lowercase)
    algo_name = hash_algorithm.lower()

    # Check if the algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is not supported.")

    # Reject known insecure algorithms
    if algo_name in INSECURE_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is considered insecure for signing.")

    # Create the HMAC object and compute the digest
    hmac_obj = hmac.new(SECRET_KEY, content, digestmod=algo_name)
    return hmac_obj.digest()