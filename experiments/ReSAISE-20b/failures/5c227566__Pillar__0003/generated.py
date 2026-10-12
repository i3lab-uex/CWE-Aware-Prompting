import hashlib
import hmac
from typing import Union

# Allowed hash algorithms (as per the description)
ALLOWED_HASHES = {
    'md5', 'sha1', 'sha256', 'blake2b',
    'ripemd160', 'sha512', 'shake_256', 'sm3',
    'sha384', 'sha3_256', 'sha512_224'
}

def create_signature(
    hash_function_name: str,
    msg: bytes,
    sec_key: bytes
) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    hash_function_name : str
        Name of the hashing function to use (e.g., 'sha256', 'md5').
    msg : bytes
        The message to sign.
    sec_key : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or unavailable.
    """
    # Normalize and validate hash function name
    alg = hash_function_name.lower()
    if alg not in ALLOWED_HASHES:
        raise ValueError(f"Unsupported hash algorithm: {hash_function_name!r}")

    # Verify that the algorithm is available in this environment
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm {hash_function_name!r} is not available in this Python build")

    # Create the HMAC object and compute the digest
    hmac_obj = hmac.new(sec_key, msg, hashlib.new(alg))
    return hmac_obj.digest()