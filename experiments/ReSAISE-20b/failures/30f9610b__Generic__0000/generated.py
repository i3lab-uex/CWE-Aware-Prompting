import hashlib
import hmac

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Sign the given message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        Name of the hash function to use (e.g. 'sha256', 'md5', etc.).
    data : bytes
        The message to be signed.
    secret_key : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or not available.
    """
    # Normalise method name
    method_name = method_name.lower()

    try:
        hash_func = getattr(hashlib, method_name)
    except AttributeError as exc:
        raise ValueError(f"Unsupported hash algorithm: {method_name}") from exc

    # Ensure the function is callable (some objects may exist but not be hash functions)
    if not callable(hash_func):
        raise ValueError(f"Hash algorithm '{method_name}' is not callable")

    # Create HMAC object and return the digest
    h = hmac.new(secret_key, data, digestmod=hash_func)
    return h.digest()