import hashlib
import hmac

# A secret key used for signing the data.
# In a real application this should be securely generated and stored.
secret_key: bytes = b"super_secret_key"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'sha512').
    data : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the data.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not available in hashlib.
    """
    # Verify that the requested algorithm exists
    if hash_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create an HMAC object using the secret key and specified hash algorithm
    h = hmac.new(secret_key, msg=data, digestmod=hash_name.lower())
    return h.digest()