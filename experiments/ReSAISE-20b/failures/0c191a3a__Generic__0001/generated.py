import hashlib
import hmac

# Example secret key – in a real application this should be kept secure and not hard‑coded.
secret_key: bytes = b"super_secret_key"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b', etc.).
    data : bytes
        The binary data to be signed.

    Returns
    -------
    bytes
        The HMAC digest (digital signature).

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Validate that the requested hash algorithm exists
    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create and return the HMAC digest
    mac = hmac.new(secret_key, data, digestmod=hash_name)
    return mac.digest()