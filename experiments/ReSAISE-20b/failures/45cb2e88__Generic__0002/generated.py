import hashlib
import hmac

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature of `content` using the specified hash algorithm
    and secret key.

    Parameters
    ----------
    algorithm : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b').
    content : bytes
        The data to sign.
    secret_key : bytes
        Secret key for the HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure algorithm name is lowercase for consistency
    algo_name = algorithm.lower()

    # Verify that the algorithm is supported by hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create the HMAC object using the chosen hash function
    hmac_obj = hmac.new(secret_key, content, hashlib.get_digest_by_name(algo_name))

    # Return the raw digest bytes
    return hmac_obj.digest()