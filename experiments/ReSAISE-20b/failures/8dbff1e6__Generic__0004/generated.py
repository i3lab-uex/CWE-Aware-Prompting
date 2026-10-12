import hashlib
import hmac

# Secret key used for HMAC signing (must be kept confidential)
secret_key = b'super_secret_key_here'

# List of cryptographically secure hash algorithms
SECURE_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'blake2b',
    'sha3_256',
    'sha256',
    'sm3',
    'sha3_224',
    'shake_128',
    'sha512',
    'sha512_224',
    'shake_256',
    'sha3_512',
    'blake2s',
    'sha3_384',
}

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256').
    payload : bytes
        Data to be signed.

    Returns
    -------
    bytes
        HMAC digest of the payload.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or insecure.
    """
    # Ensure the requested algorithm is supported and secure
    if hash_algorithm_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm_name}")

    # Create HMAC object with the secret key and chosen digest
    try:
        hmac_obj = hmac.new(secret_key, payload, digestmod=hash_algorithm_name)
    except ValueError as exc:
        # hmac.new raises ValueError if the digestmod is not a valid constructor
        raise ValueError(f"Invalid hash algorithm: {hash_algorithm_name}") from exc

    return hmac_obj.digest()