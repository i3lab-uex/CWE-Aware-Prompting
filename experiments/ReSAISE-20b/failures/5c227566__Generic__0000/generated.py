import hmac
import hashlib

def create_signature(hash_function_name: str, msg: bytes, sec_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    hash_function_name : str
        Name of the hash function to use (e.g., 'sha256', 'md5').
    msg : bytes
        The message to be signed.
    sec_key : bytes
        Secret key used in the HMAC process.

    Returns
    -------
    bytes
        The computed HMAC signature as raw bytes.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Ensure the requested hash function is available
    try:
        digest_mod = hashlib.new(hash_function_name)
    except ValueError as exc:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: {hash_function_name}"
        ) from exc

    # Compute HMAC
    hmac_obj = hmac.new(sec_key, msg, digest_mod)
    return hmac_obj.digest()