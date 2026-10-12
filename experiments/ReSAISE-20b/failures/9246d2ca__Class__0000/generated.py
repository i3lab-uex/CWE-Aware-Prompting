import hashlib

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the requested algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hashing algorithm to use. Must be one of the algorithms returned by
        ``hashlib.algorithms_available``.
    pass_key : bytes
        The password (or key material) to hash.

    Returns
    -------
    bytes
        The raw digest produced by the chosen algorithm.

    Raises
    ------
    ValueError
        If *algo_name* is not a supported algorithm.
    """
    # Normalise the name to lower‑case, as hashlib is case‑insensitive but the
    # set of available names may use different casing.
    algo = algo_name.lower()

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name!r}")

    # ``hashlib.new`` accepts the algorithm name and the initial data.
    hasher = hashlib.new(algo, pass_key)
    return hasher.digest()