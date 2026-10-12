import hashlib
import hmac

# A secret key used for HMAC signing (must be kept confidential in production)
SECRET_KEY: bytes = b'super-secret-key'

# List of cryptographic hash algorithms that are considered secure for signing
SECURE_ALGORITHMS = {
    'sha224', 'sha256', 'sha384', 'sha512',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
    'blake2b', 'blake2s', 'sm3'
}

def create_signature(algo_name: str, raw_data: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified secure hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hashing algorithm to use. Must be one of the secure algorithms.
    raw_data : bytes
        The data that needs to be signed.

    Returns
    -------
    bytes
        The resulting HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or considered insecure.
    """
    algo_name_lower = algo_name.lower()
    if algo_name_lower not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algo_name}")

    # Create a new HMAC object with the chosen algorithm and secret key
    try:
        h = hmac.new(SECRET_KEY, raw_data, getattr(hashlib, algo_name_lower))
    except AttributeError as exc:
        # hashlib may not expose the algorithm directly (e.g., 'sha512_256')
        raise ValueError(f"Algorithm '{algo_name}' is not available in hashlib") from exc

    return h.digest()