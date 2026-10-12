import hashlib
import hmac

def sign_message(hash_name: str, message: bytes, key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'sha512_256').
    message : bytes
        The message to be signed.
    key : bytes
        Secret key used for signing.

    Returns
    -------
    bytes
        The HMAC digest of the message.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Normalise the algorithm name to lower case for comparison
    alg_name = hash_name.lower()

    # Check that the algorithm is available in the current Python build
    if alg_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create the HMAC object using the provided key, message and hash algorithm
    hmac_obj = hmac.new(key, msg=message, digestmod=alg_name)

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()