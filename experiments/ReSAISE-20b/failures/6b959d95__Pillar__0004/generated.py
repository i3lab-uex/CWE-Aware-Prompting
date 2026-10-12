import hashlib
import hmac

# List of algorithms that the environment claims to support.
_SUPPORTED_ALGORITHMS = {name.lower() for name in hashlib.algorithms_available}

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC of *content* using the specified *algorithm* and *secret* key.

    Parameters
    ----------
    algorithm : str
        The name of the hash algorithm to use (e.g., 'sha256', 'md5').
    content : bytes
        The message to sign.
    secret : bytes
        The key used for the HMAC calculation.

    Returns
    -------
    bytes
        The raw HMAC digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the underlying hashlib implementation.
    """
    if not isinstance(algorithm, str):
        raise TypeError("algorithm must be a string")
    if not isinstance(content, bytes) or not isinstance(secret, bytes):
        raise TypeError("content and secret must be of type 'bytes'")

    algo = algorithm.lower()
    if algo not in _SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # hmac.new accepts a digestmod argument that can be a string name.
    mac = hmac.new(secret, msg=content, digestmod=algo)
    return mac.digest()