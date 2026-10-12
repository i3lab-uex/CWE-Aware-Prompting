import hashlib
import hmac

def sign_message(hash_name: str, message: bytes, key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        The message to be signed.
    key : bytes
        Secret key used for signing.

    Returns
    -------
    bytes
        The HMAC signature of the message.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Ensure the hash algorithm exists
    if hash_name.lower() not in {alg.lower() for alg in hashlib.algorithms_available}:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create an HMAC object using the chosen hash function
    h = hmac.new(key, msg=message, digestmod=hash_name)
    return h.digest()