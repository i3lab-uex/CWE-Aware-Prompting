import hashlib
import hmac
from typing import Any

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC value for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        The secret key used for HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported on this system.
    """
    # Normalise algorithm name to lowercase for comparison
    algo = algorithm_name.lower()

    # Verify that the requested algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create the HMAC object with the chosen digest method
    hmac_obj = hmac.new(secret_key, msg_content, digestmod=algo)

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()