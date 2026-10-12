import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC of `msg_content` using the specified hash algorithm and `secret_key`.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2s', ...).
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        Secret key used for HMAC generation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in the current Python environment.
    """
    # Normalise algorithm name (case‑insensitive)
    algo = algorithm_name.lower()

    # Verify the algorithm is available
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not supported on this system")

    # Compute the HMAC
    return hmac.new(secret_key, msg_content, digestmod=algo).digest()