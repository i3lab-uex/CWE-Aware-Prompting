import hashlib
import hmac

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC value for the given message using the specified hash algorithm.

    Parameters
    ----------
    algo : str
        Name of the hash algorithm to use (e.g. 'sha256', 'md5', etc.).
    msg : bytes
        The message to authenticate.
    secret_key : bytes
        Secret key used for HMAC generation.

    Returns
    -------
    bytes
        The computed HMAC digest of the message.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by the underlying
        hashlib implementation.
    """
    # Normalise algorithm name to lower‑case for comparison
    algo_name = algo.lower()

    # Verify that the requested algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    # Compute the HMAC using the specified digest
    return hmac.new(secret_key, msg, digestmod=algo_name).digest()