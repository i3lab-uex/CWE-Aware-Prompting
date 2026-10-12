import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute the HMAC of a message using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        The secret key used for HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC digest as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by the underlying hashlib implementation.
    """
    # Normalise algorithm name to lower case
    algo = algorithm_name.lower()

    # Verify that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create and compute the HMAC
    hmac_obj = hmac.new(secret_key, msg_content, digestmod=algo)
    return hmac_obj.digest()