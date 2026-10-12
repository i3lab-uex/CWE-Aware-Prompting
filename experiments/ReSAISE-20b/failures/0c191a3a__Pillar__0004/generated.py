import hashlib
import hmac

# Secret key used for signing (in a real system this should be stored securely)
secret_key = b"your-very-secret-key"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for `data` using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use (e.g. 'sha256', 'sha512').
    data : bytes
        The payload to sign.

    Returns
    -------
    bytes
        The HMAC digest (digital signature).

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Verify that the algorithm exists in the standard library
    if hash_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available in hashlib.")

    # Create an HMAC object with the chosen hash algorithm
    h = hmac.new(secret_key, data, getattr(hashlib, hash_name.lower()))
    return h.digest()