import hashlib
import hmac

# Allowed cryptographic hash algorithms (excluding known weak ones such as md5 and sha1)
ALLOWED_HASH_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'blake2b',
    'blake2s',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
}

def generate_token(hash_algorithm_name: str, payload: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given payload using a secure hash algorithm.

    Args:
        hash_algorithm_name: Name of the hash algorithm to use.
        payload: Data to be signed (bytes).
        secret_key: Key used for HMAC signing (bytes).

    Returns:
        The HMAC digest as bytes.

    Raises:
        ValueError: If the specified hash algorithm is not supported or considered insecure.
    """
    # Validate the requested hash algorithm
    if hash_algorithm_name not in ALLOWED_HASH_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {hash_algorithm_name!r}. "
            f"Allowed algorithms are: {', '.join(sorted(ALLOWED_HASH_ALGORITHMS))}"
        )

    # Create the HMAC object with the selected hash algorithm
    try:
        hmac_obj = hmac.new(secret_key, payload, digestmod=hashlib.new(hash_algorithm_name))
    except Exception as exc:
        # In practice, this should never happen for the allowed algorithms
        raise ValueError(f"Failed to create HMAC: {exc}") from exc

    return hmac_obj.digest()