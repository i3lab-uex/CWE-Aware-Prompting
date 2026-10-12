import hmac
import hashlib

# Set of hash algorithm names that are considered safe for HMAC usage.
# These correspond to the algorithms available in hashlib on most Python
# implementations.  The set can be extended if new safe algorithms are added.
SAFE_HASH_ALGORITHMS = {
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
    'sha512_224',
}

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for *data* using the specified hash algorithm
    and a secret key.

    Parameters:
        method_name (str): Name of the hash algorithm to use.
                           Must be one of the names in SAFE_HASH_ALGORITHMS.
        data (bytes): The message to sign.
        secret_key (bytes): Secret key used in the HMAC calculation.

    Returns:
        bytes: The resulting HMAC signature.

    Raises:
        ValueError: If *method_name* is not supported or not available.
    """
    # Normalise the method name to lower case for comparison
    algo = method_name.lower()

    if algo not in SAFE_HASH_ALGORITHMS:
        raise ValueError(f"Unsupported hash algorithm: {method_name!r}")

    # Retrieve the constructor for the hash function from hashlib.
    # This raises a TypeError if the algorithm is not available on the
    # current platform, which we convert to ValueError for clarity.
    try:
        hash_func = getattr(hashlib, algo)
    except AttributeError as exc:
        raise ValueError(f"Hash algorithm {method_name!r} is not available") from exc

    # Create and return the HMAC digest
    return hmac.new(secret_key, data, hash_func).digest()