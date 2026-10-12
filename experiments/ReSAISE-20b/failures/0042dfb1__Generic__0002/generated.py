import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'md5').
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        The secret key used in the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC value of the message.

    Raises
    ------
    ValueError
        If the selected hash algorithm is not supported.
    """
    # Normalise the algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    # Check that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Compute the HMAC using the selected digest module
    h = hmac.new(secret_key, msg_content, digestmod=algo)
    return h.digest()