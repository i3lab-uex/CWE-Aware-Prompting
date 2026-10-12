import hashlib
import hmac

def generate_signature(hash_algo: str, input_data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    hash_algo : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    input_data : bytes
        The data to be signed.
    secret_key : bytes
        The secret key used for signing.

    Returns
    -------
    bytes
        The computed HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    TypeError
        If any of the arguments are not of the expected type.
    """
    # Basic type checks for clarity and safety
    if not isinstance(hash_algo, str):
        raise TypeError("hash_algo must be a string")
    if not isinstance(input_data, bytes):
        raise TypeError("input_data must be bytes")
    if not isinstance(secret_key, bytes):
        raise TypeError("secret_key must be bytes")

    # Ensure the algorithm is supported by hashlib
    if hash_algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo}")

    # Create the HMAC object and return the digest
    hmac_obj = hmac.new(secret_key, input_data, getattr(hashlib, hash_algo.lower()))
    return hmac_obj.digest()