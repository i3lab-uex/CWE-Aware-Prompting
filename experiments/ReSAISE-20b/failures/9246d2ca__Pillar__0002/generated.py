import hashlib
from typing import Union

def encrypt_password(algo_name: str, pass_key: bytes) -> bytes:
    """
    Compute a cryptographic hash of ``pass_key`` using the algorithm
    specified by ``algo_name``.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    pass_key : bytes
        The password or data to be hashed.

    Returns
    -------
    bytes
        The digest produced by the chosen hash algorithm.

    Raises
    ------
    ValueError
        If ``algo_name`` is not supported by the current Python build.
    TypeError
        If ``pass_key`` is not of type `bytes`.

    Notes
    -----
    The function checks the set of algorithms available on the current
    interpreter (``hashlib.algorithms_available``).  This guards against
    attempting to use algorithms that are missing from the underlying OpenSSL
    library, which could otherwise result in a cryptographic failure.
    """
    if not isinstance(pass_key, bytes):
        raise TypeError("pass_key must be of type 'bytes'")

    # Normalise algorithm name to lowercase; hashlib is case‑insensitive
    algo_name = algo_name.lower()

    # Ensure the requested algorithm exists on this platform
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo_name}")

    # Compute the digest
    hasher = hashlib.new(algo_name)
    hasher.update(pass_key)
    return hasher.digest()