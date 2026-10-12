import hashlib
import hmac

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        Name of the hashing algorithm to use (e.g. 'sha256', 'md5').
    data : bytes
        The message to be signed.
    secret_key : bytes
        Secret key used in the HMAC calculation.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or available.
    """
    if not isinstance(method_name, str):
        raise TypeError("method_name must be a string")
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if not isinstance(secret_key, bytes):
        raise TypeError("secret_key must be bytes")

    # Normalize method name to lower case for consistency
    algo = method_name.lower()

    # Verify that the algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {method_name}")

    # Create the HMAC object using the selected digest method
    hmac_obj = hmac.new(secret_key, data, digestmod=algo)

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()