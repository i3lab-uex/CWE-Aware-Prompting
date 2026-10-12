import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC of the given message using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2s').
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        The key used for the HMAC computation.

    Returns
    -------
    bytes
        The binary digest of the computed HMAC.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in the current Python environment.
    """
    # Normalize algorithm name to lower case for lookup
    alg = algorithm_name.lower()

    # Ensure the requested algorithm is supported by hashlib
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create HMAC object and compute digest
    hmac_obj = hmac.new(secret_key, msg_content, digestmod=alg)
    return hmac_obj.digest()