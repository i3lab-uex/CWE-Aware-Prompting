import hashlib
import hmac

def create_signature(hash_function_name: str, msg: bytes, sec_key: bytes) -> bytes:
    """
    Create an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    hash_function_name : str
        Name of the hash function to use (e.g., 'sha256', 'md5', etc.).
    msg : bytes
        The message to sign.
    sec_key : bytes
        Secret key for the HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the hash function name is in a canonical form
    algo_name = hash_function_name.lower()

    # Check if the algorithm is supported by hashlib
    try:
        hash_func = getattr(hashlib, algo_name)
    except AttributeError:
        raise ValueError(f"Hash algorithm '{hash_function_name}' is not supported.") from None

    # Create the HMAC object using the chosen hash function
    hmac_obj = hmac.new(sec_key, msg=msg, digestmod=hash_func)

    # Return the binary digest
    return hmac_obj.digest()