import os
import hashlib
import hmac

# A secure, random secret key for HMAC signing.
# In a real application this should be stored securely and not regenerated each run.
SECRET_KEY: bytes = os.urandom(32)

# List of algorithms considered weak for cryptographic signing purposes.
_WEAK_ALGORITHMS = {
    "md5",
    "sha1",
    "ripemd160",
    "md5-sha1",  # composite algorithm containing MD5
}

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for the provided data using a secure hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        The desired hash algorithm (e.g., 'sha256', 'sha512_256').
    content : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC digest of the content using the specified hash algorithm.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not available or is considered weak.
    """
    # Normalise algorithm name to lower case
    algo = hash_algorithm.lower()

    # Check that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is not supported by hashlib.")

    # Reject known weak algorithms
    if algo in _WEAK_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{hash_algorithm}' is considered insecure for signing.")

    # Compute the HMAC digest
    try:
        hmac_obj = hmac.new(SECRET_KEY, content, digestmod=algo)
    except ValueError as exc:
        # hmac may raise ValueError if the digestmod string is invalid
        raise ValueError(f"Failed to create HMAC with algorithm '{hash_algorithm}': {exc}") from exc

    return hmac_obj.digest()