import hashlib
import hmac

# NOTE: In a real application this key should be securely stored and managed.
# For demonstration purposes we define it here as a constant.  Replace this
# with your own secure key management solution.
secret_key = b"super_secret_key_used_for_signing"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC and the
    specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    data : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC digest (digital signature).

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the requested hash algorithm is available
    if hash_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new HMAC object using the chosen hash algorithm
    h = hmac.new(secret_key, data, getattr(hashlib, hash_name.lower()))
    return h.digest()