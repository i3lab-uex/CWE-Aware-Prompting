import hashlib
import hmac

def sign_message(hash_name: str, message: bytes, key: bytes) -> bytes:
    """
    Sign a message using the specified hash algorithm and secret key.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b', etc.).
    message : bytes
        The message to be signed.
    key : bytes
        The secret key used for signing.

    Returns
    -------
    bytes
        The HMAC digest of the message using the specified hash algorithm.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in the current Python
        installation.
    """
    # Normalise the hash name to lower case as required by hashlib
    algo = hash_name.lower()

    # Check if the algorithm is supported
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Use HMAC to compute a secure message authentication code
    mac = hmac.new(key, message, algo)
    return mac.digest()