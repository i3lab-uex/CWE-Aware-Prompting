import hashlib
import hmac

# A set of algorithms that are considered weak or broken.
_WEAK_ALGORITHMS = {
    'md5',
    'sha1',
    'md4',          # not in hashlib by default, but listed for completeness
    'sha224',
}

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature of `content` using the specified `algorithm`
    and `secret_key`.

    Parameters
    ----------
    algorithm : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b').
    content : bytes
        The data to sign.
    secret_key : bytes
        Secret key for the HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.

    Notes
    -----
    The function performs a quick check to see if the algorithm is available
    via `hashlib.new`.  If it is not, a ValueError is raised.  A warning
    (printed to stderr) is issued if the algorithm is known to be weak.
    """
    # Validate that the algorithm exists in hashlib
    try:
        hashlib.new(algorithm)
    except ValueError as exc:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}") from exc

    # Optional: warn about weak algorithms
    if algorithm.lower() in _WEAK_ALGORITHMS:
        import warnings
        warnings.warn(
            f"The algorithm '{algorithm}' is considered weak and may not be suitable "
            "for cryptographic purposes.",
            RuntimeWarning,
        )

    # Compute HMAC
    return hmac.new(secret_key, content, algorithm).digest()