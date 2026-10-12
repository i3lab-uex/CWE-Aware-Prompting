import hashlib
import hmac

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC of *msg* using the specified hash algorithm and secret key.

    Parameters
    ----------
    algo : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2s').
    msg : bytes
        The message to be authenticated.
    secret_key : bytes
        Secret key for the HMAC.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not available on this system.
    """
    # Ensure the algorithm name is valid
    if algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    # Use hmac with the specified digestmod; this guarantees constant‑time
    # comparison when needed by callers (hmac.compare_digest).
    h = hmac.new(secret_key, msg, digestmod=algo)
    return h.digest()