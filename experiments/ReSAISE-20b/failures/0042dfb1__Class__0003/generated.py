import hashlib
import hmac

# Supported hash algorithms that are available via hashlib.new()
_SUPPORTED_ALGORITHMS = {
    name for name in hashlib.algorithms_available
    if name not in {"shake_128", "shake_256"}  # variable length hashes are excluded
}

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC value for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2s').
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        The secret key for HMAC generation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported on this system.
    """
    # Normalise algorithm name to lower case and validate
    algo = algorithm_name.lower()
    if algo not in _SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Compute the HMAC using the chosen digest
    return hmac.new(secret_key, msg_content, digestmod=algo).digest()