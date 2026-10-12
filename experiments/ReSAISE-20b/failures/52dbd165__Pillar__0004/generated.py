import hashlib
import hmac

def generate_signature(hash_algo: str, input_data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use (e.g., 'sha256', 'blake2s').
    input_data : bytes
        The data to sign.
    secret_key : bytes
        The secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported by hashlib.
    """
    # Normalize algorithm name to lower case for consistency
    algo_name = hash_algo.lower()

    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo}")

    # Create a new hash object for the specified algorithm
    hash_func = hashlib.new(algo_name)

    # Compute HMAC using the provided key and data
    return hmac.new(secret_key, input_data, hash_func).digest()