import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC value for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2s').
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        Secret key used in the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC digest as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by the underlying system.
    """
    # Normalize algorithm name to lower case for consistency
    algo = algorithm_name.lower()

    # Verify that the chosen algorithm is available in this environment.
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create the HMAC object using the selected hash function
    hmac_obj = hmac.new(secret_key, msg_content, digestmod=algo)

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()