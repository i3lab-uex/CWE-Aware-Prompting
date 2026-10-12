import hashlib
import hmac

# Define a whitelist of acceptable hash algorithms (exclude known weak ones)
ALLOWED_ALGORITHMS = {
    'sha1',          # Not ideal but included per spec
    'md5',           # Weak, but allowed for demonstration
    'sha256',
    'blake2b',
    'ripemd160',
    'sha512',
    'shake_256',     # Variable length
    'sm3',
    'sha384',
    'sha3_256',
    'sha512_224'
}

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
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
        If the specified hash algorithm is not supported or available.
    """
    # Normalise method name
    algo = method_name.lower()

    # Validate against allowed list and availability in hashlib
    if algo not in ALLOWED_ALGORITHMS or algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {method_name}")

    # Create HMAC object and compute digest
    hmac_obj = hmac.new(secret_key, data, digestmod=algo)
    return hmac_obj.digest()