import hashlib
import hmac

def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        Data to be signed.
    secret : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Normalise algorithm name to lower case for lookup
    algo_name = hash_algorithm.lower()

    # Check if the algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create a new HMAC object with the chosen hash function
    hmac_obj = hmac.new(secret, payload, digestmod=algo_name)

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()