import hashlib
import hmac

def generate_signature(hash_algo: str, input_data: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use (e.g., 'sha256', 'blake2s').
    input_data : bytes
        The data to be signed.
    secret_key : bytes
        The secret key used for signing.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Verify that the requested algorithm is available
    if hash_algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo}")

    # Create a new HMAC object using the specified hash function
    hmac_obj = hmac.new(secret_key, input_data, digestmod=hash_algo.lower())

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()