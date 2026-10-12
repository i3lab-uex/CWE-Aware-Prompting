import hashlib
import hmac

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute the HMAC of a message using the specified hash algorithm and secret key.

    Parameters
    ----------
    algo : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2s').
    msg : bytes
        The message to authenticate.
    secret_key : bytes
        The secret key used for HMAC computation.

    Returns
    -------
    bytes
        The HMAC digest of the message.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported by the underlying hashlib implementation.
    """
    # Ensure the algorithm name is case-insensitive and strip whitespace
    algo_clean = algo.strip().lower()

    # Verify that the algorithm is supported by hashlib
    if algo_clean not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo!r}")

    # Compute HMAC using the specified algorithm
    hmac_obj = hmac.new(secret_key, msg, digestmod=algo_clean)
    return hmac_obj.digest()