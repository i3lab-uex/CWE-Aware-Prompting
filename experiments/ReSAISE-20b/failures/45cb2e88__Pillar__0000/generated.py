import hmac
import hashlib
from typing import Iterable

# List of hash algorithms supported by the current Python environment
_SUPPORTED_ALGORITHMS: set[str] = {
    name.lower() for name in hashlib.algorithms_available
}

def create_hmac_signature(
    algorithm: str,
    content: bytes,
    secret_key: bytes
) -> bytes:
    """
    Compute an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b').
    content : bytes
        The data to sign.
    secret_key : bytes
        Secret key used for the HMAC.

    Returns
    -------
    bytes
        The raw HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    if not isinstance(algorithm, str):
        raise TypeError("Algorithm must be a string")
    algo_name = algorithm.lower()
    if algo_name not in _SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm!r}")

    # Create a new HMAC object using the requested digest
    try:
        hash_func = hashlib.new(algo_name)
    except (ValueError, TypeError):
        # Fallback: some algorithms may need to be referenced by alias
        raise ValueError(f"Unsupported hash algorithm: {algorithm!r}")

    hmac_obj = hmac.new(secret_key, content, hash_func)
    return hmac_obj.digest()