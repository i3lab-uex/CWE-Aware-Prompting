import hashlib
import hmac

def compute_hmac(algorithm_name: str, msg_content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC of `msg_content` using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2s', etc.).
    msg_content : bytes
        The message to be authenticated.
    secret_key : bytes
        Secret key used for HMAC calculation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by the underlying hashlib.
    """
    # Ensure algorithm name is case‑insensitive and strip whitespace
    algo = algorithm_name.strip().lower()

    # Verify the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create a new HMAC object with the chosen digest method
    h = hmac.new(secret_key, msg_content, digestmod=algo)

    # Return the raw bytes of the HMAC
    return h.digest()