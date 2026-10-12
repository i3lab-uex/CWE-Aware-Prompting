import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute the HMAC of a message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        Secret key used for HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or inputs are invalid.
    """
    if not isinstance(algorithm_name, str):
        raise ValueError("algorithm_name must be a string")
    if not isinstance(msg_content, bytes):
        raise ValueError("msg_content must be bytes")
    if not isinstance(secret_key, bytes):
        raise ValueError("secret_key must be bytes")

    # Normalize algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    # Check if the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create HMAC object with the selected digest
    hmac_obj = hmac.new(secret_key, msg_content, digestmod=algo)

    return hmac_obj.digest()