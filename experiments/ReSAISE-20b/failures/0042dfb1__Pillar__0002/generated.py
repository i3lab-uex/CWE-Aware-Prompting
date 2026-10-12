import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC of the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'md5').
    msg_content : bytes
        The message to authenticate.
    secret_key : bytes
        The secret key used in the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC value (raw digest).

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available on this system.
    """
    # Normalize algorithm name to lower case
    algo = algorithm_name.lower()

    # Ensure the algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create the HMAC object using the specified algorithm
    hmac_obj = hmac.new(secret_key, msg_content, digestmod=algo)

    # Return the raw digest bytes
    return hmac_obj.digest()