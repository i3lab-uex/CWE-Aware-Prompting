import hashlib
import hmac

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC of *msg* using the specified hash algorithm and secret key.

    Parameters
    ----------
    algo : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2s').
    msg : bytes
        The message to authenticate.
    secret_key : bytes
        The secret key used for HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC value.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in the current Python runtime.
    """
    # Normalise the algorithm name to lower‑case as used by hashlib
    algo = algo.lower()

    # Verify that the requested algorithm is supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo!r}")

    # Use the hmac module which implements constant‑time comparison internally
    return hmac.new(secret_key, msg, digestmod=algo).digest()