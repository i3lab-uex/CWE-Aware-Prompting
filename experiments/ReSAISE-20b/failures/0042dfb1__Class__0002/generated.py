import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute the HMAC of a message using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2s').
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        The secret key used in the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC value (raw digest).

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by the system.
    """
    # Normalize algorithm name to lower case for lookup
    alg = algorithm_name.lower()

    # Verify that the requested algorithm is available in hashlib
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Compute the HMAC using the specified algorithm
    mac = hmac.new(secret_key, msg_content, digestmod=alg)
    return mac.digest()