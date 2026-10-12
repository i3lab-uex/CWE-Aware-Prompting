import hashlib
import hmac

def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'blake2s').
    payload : bytes
        Data to be signed.
    secret : bytes
        Secret key for HMAC.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported by hashlib.
    """
    # Normalise algorithm name to lowercase for consistency
    algo_name = hash_algorithm.lower()

    # Verify that the algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create a new HMAC object with the given secret and hash function
    try:
        hmac_obj = hmac.new(secret, payload, digestmod=algo_name)
    except Exception as exc:
        # Wrap any lower‑level errors in a ValueError to keep the API consistent
        raise ValueError(f"Failed to compute HMAC: {exc}") from exc

    return hmac_obj.digest()