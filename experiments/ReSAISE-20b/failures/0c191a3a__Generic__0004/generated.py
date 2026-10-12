import hashlib
import hmac

# Secret key used for signing – in a real application this should be kept secure
secret_key: bytes = b"my_very_secret_key"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b').
    data : bytes
        The message to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the data.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not available in hashlib.
    """
    # Normalise the hash name for comparison
    norm_name = hash_name.lower()

    if norm_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new hash object for the chosen algorithm
    hash_func = hashlib.new(norm_name)

    # Compute HMAC using the secret key and the chosen hash function
    signature = hmac.new(secret_key, data, digestmod=hash_func).digest()
    return signature