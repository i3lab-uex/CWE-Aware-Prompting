import hashlib
import hmac

# Allowed hash algorithms.  If a method is not available on the system,
# hashlib.new will raise ValueError.
ALLOWED_HASHES = {
    'md5',
    'sha1',
    'sha256',
    'blake2b',
    'ripemd160',
    'sha512',
    'shake_256',
    'sm3',
    'sha384',
    'sha3_256',
    'sha512_224'
}


def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for *data* using the specified hash algorithm
    and *secret_key*.

    Parameters
    ----------
    method_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    data : bytes
        The message to sign.
    secret_key : bytes
        Secret key for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If *method_name* is not supported or unavailable on the current system.
    """
    if method_name.lower() not in ALLOWED_HASHES:
        raise ValueError(f"Unsupported hash algorithm: {method_name}")

    # Ensure the requested hash function is available
    try:
        hashlib.new(method_name)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{method_name}' is not available.") from exc

    # Create the HMAC object using the provided key, data, and digest method
    h = hmac.new(secret_key, msg=data, digestmod=method_name)
    return h.digest()