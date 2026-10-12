import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2s').
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        Secret key used for HMAC generation.

    Returns
    -------
    bytes
        The computed HMAC value.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported on this system.
    """
    # Normalise algorithm name to lowercase for comparison
    algo = algorithm_name.lower()

    # Check if the requested algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create the HMAC object and compute the digest
    hmac_obj = hmac.new(secret_key, msg_content, digestmod=algo)
    return hmac_obj.digest()