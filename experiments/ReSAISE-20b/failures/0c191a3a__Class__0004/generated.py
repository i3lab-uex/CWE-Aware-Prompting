import hashlib
import hmac

# Secret key used for signing (must be kept confidential)
secret_key: bytes = b"your-very-secure-secret-key"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'sha512_224', etc.).
    data : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC digest of the data using the chosen hash algorithm.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Verify that the requested algorithm exists
    if hash_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Compute HMAC using the specified hash function
    h = hmac.new(secret_key, data, digestmod=hash_name)
    return h.digest()