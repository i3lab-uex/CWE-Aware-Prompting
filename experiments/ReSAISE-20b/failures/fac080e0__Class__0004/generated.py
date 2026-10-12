import hashlib
import hmac

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC of *msg* using the specified hash algorithm and secret key.

    Parameters
    ----------
    algo : str
        The name of the hash algorithm to use (e.g. 'sha256', 'blake2s').
    msg : bytes
        The message to authenticate.
    secret_key : bytes
        The secret key used in the HMAC calculation.

    Returns
    -------
    bytes
        The computed HMAC value (raw digest).

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by this Python installation.
    """
    # Ensure the algorithm name is case‑insensitive
    algo = algo.lower()

    # Verify that the requested hash algorithm exists in this environment.
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    # Use the hmac module to compute a secure HMAC
    mac = hmac.new(secret_key, msg, getattr(hashlib, algo))
    return mac.digest()