import hashlib
import hmac

def create_signature(hash_function_name: str, msg: bytes, sec_key: bytes) -> bytes:
    """
    Generate an HMAC signature for `msg` using the specified hash algorithm and secret key.

    Parameters
    ----------
    hash_function_name : str
        Name of the hashing algorithm to use (e.g., 'sha256', 'md5').
    msg : bytes
        The message to sign.
    sec_key : bytes
        Secret key for the HMAC.

    Returns
    -------
    bytes
        The raw HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or unavailable.
    """
    # Normalize name to lowercase
    alg = hash_function_name.lower()

    # Check availability of the algorithm
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_function_name}")

    # Create HMAC object with the chosen hash function
    try:
        hmac_obj = hmac.new(sec_key, msg, digestmod=alg)
    except Exception as exc:
        # Wrap any lower‑level errors in ValueError for consistency
        raise ValueError(f"Failed to create HMAC: {exc}") from exc

    return hmac_obj.digest()