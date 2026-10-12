import hashlib
import hmac

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute the HMAC of ``msg`` using ``secret_key`` and the hash algorithm
    specified by ``algo``.

    Parameters
    ----------
    algo : str
        Name of the hash algorithm (e.g. 'sha256', 'blake2s', ...).
    msg : bytes
        The message to authenticate.
    secret_key : bytes
        Secret key used for the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not available on this system.
    """
    # Ensure the algorithm name is valid and supported by hashlib
    if algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    # Compute the HMAC using the selected hash function
    hmac_obj = hmac.new(secret_key, msg, getattr(hashlib, algo.lower()))
    return hmac_obj.digest()