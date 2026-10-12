import hashlib
import hmac

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        The name of the hashing algorithm to use (e.g. 'sha256', 'md5').
    data : bytes
        The message to be signed.
    secret_key : bytes
        The secret key used in the HMAC process.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or requires a digest length.
    """
    # Normalise name to lowercase
    algo = method_name.lower()

    # Check availability and avoid algorithms that require a digest length
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{method_name}' is not available.")
    if algo in {"shake_128", "shake_256"}:
        raise ValueError(f"Algorithm '{method_name}' requires a digest length; "
                         "not supported in this function.")

    # Create HMAC object
    h = hmac.new(secret_key, data, digestmod=algo)

    # Return the raw bytes of the signature
    return h.digest()