import hashlib
import hmac

# Secret key used for signing (in a real application this should be stored securely)
secret_key: bytes = b"my_super_secret_key"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (must be supported by hashlib).
    data : bytes
        The data to sign.

    Returns
    -------
    bytes
        The HMAC signature of the data.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Validate that the requested hash algorithm exists
    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new HMAC object using the chosen hash algorithm
    h = hmac.new(secret_key, digestmod=hashlib.new(hash_name))
    h.update(data)
    return h.digest()