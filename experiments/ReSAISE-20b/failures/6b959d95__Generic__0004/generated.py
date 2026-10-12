import hashlib
import hmac

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC of `content` using the given hash algorithm and secret key.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g. 'sha256', 'md5').
    content : bytes
        The message to authenticate.
    secret : bytes
        Secret key for HMAC generation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported.
    """
    # Normalise the algorithm name to lower case for consistency
    algo_name = algorithm.lower()

    # Check if the requested algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Compute the HMAC using the specified digest method
    hmac_obj = hmac.new(secret, content, digestmod=algo_name)
    return hmac_obj.digest()