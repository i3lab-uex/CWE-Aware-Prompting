import hashlib
import hmac

# List of supported algorithms that are available in the current environment.
_SUPPORTED_ALGORITHMS = {alg.lower() for alg in hashlib.algorithms_available}

def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute the HMAC signature of *payload* using *secret* and
    the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function (case‑insensitive). Must be supported by
        :mod:`hashlib`.
    payload : bytes
        The data to sign.
    secret : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported.
    """
    algo = hash_algorithm.lower()
    if algo not in _SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # ``hmac.new`` accepts either a callable or the name of the algorithm.
    return hmac.new(secret, payload, digestmod=algo).digest()