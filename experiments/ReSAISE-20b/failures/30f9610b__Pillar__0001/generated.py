import hashlib
import hmac

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Produce an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'md5').
    data : bytes
        The message to be signed.
    secret_key : bytes
        The secret key used in the HMAC computation.

    Returns
    -------
    bytes
        The resulting HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or unavailable.
    """
    # Normalise method name to lower case for consistency
    algo = method_name.lower()

    # Check if the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{method_name}' is not supported or unavailable.")

    # Use the hashlib constructor to create a hash object
    try:
        digestmod = hashlib.new(algo).name  # This ensures the algorithm exists
    except Exception as exc:
        raise ValueError(f"Failed to initialise hash algorithm '{method_name}': {exc}") from exc

    # Compute HMAC using the specified digestmod
    hmac_obj = hmac.new(secret_key, data, digestmod)
    return hmac_obj.digest()