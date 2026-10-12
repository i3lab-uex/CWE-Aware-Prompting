import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC of a message using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2s').
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        The secret key for the HMAC.

    Returns
    -------
    bytes
        The computed HMAC value.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the underlying hashlib implementation.
    """
    # Normalise algorithm name to lower case
    algo = algorithm_name.lower()

    # Verify the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Compute HMAC
    return hmac.new(secret_key, msg_content, digestmod=algo).digest()