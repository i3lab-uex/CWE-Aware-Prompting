import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC value for a message using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g. 'sha256', 'md5').
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        The secret key used in the HMAC calculation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by the current Python environment.
    """
    # Ensure the algorithm name is case‑insensitive
    algo = algorithm_name.lower()

    # Verify that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name!r}")

    # Use the hmac module which handles key normalization and constant‑time comparison
    # The hash constructor is supplied via hashlib.new.
    h = hmac.new(secret_key, msg_content, digestmod=hashlib.new(algo))
    return h.digest()