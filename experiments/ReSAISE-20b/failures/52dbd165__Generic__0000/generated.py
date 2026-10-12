import hashlib
import hmac

def generate_signature(hash_algo: str, input_data: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for the given input data using the specified hash algorithm.

    Parameters
    ----------
    hash_algo : str
        The name of the hash function to use (e.g., 'sha256', 'blake2b').
    input_data : bytes
        The data to be signed.
    secret_key : bytes
        The key used for HMAC signing.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the hash algorithm is available
    if hash_algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo}")

    # Create a new HMAC object using the specified digest mode
    hmac_obj = hmac.new(secret_key, input_data, digestmod=hashlib.new(hash_algo))
    return hmac_obj.digest()