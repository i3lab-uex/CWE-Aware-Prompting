import hashlib
import hmac

def generate_signature(hash_algo: str, input_data: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for `input_data` using the specified hash algorithm
    and secret key.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use (e.g., 'sha256', 'blake2s').
    input_data : bytes
        The data to be signed.
    secret_key : bytes
        Secret key used for the HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Normalise the hash name (hashlib accepts lower‑case names)
    algo_name = hash_algo.lower()

    # Verify that the algorithm is supported
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo!r}")

    # Compute the HMAC
    return hmac.new(secret_key, input_data, digestmod=algo_name).digest()