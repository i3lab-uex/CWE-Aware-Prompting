import hashlib
import hmac

def generate_signature(hash_algo: str, input_data: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature of the given data using the specified hash algorithm.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b', etc.).
    input_data : bytes
        The data to be signed.
    secret_key : bytes
        The secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Normalise algorithm name to lower case (hashlib uses lower‑case names)
    algo_name = hash_algo.lower()

    # Verify that the algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo}")

    # Create the HMAC object and compute the digest
    hmac_obj = hmac.new(secret_key, input_data, hashlib.new(algo_name))
    return hmac_obj.digest()