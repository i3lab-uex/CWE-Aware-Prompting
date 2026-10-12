import hashlib
import hmac

# Set of cryptographically secure hash algorithms supported by this function.
SECURE_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
}

def create_checksum(algorithm_name: str, message_data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message data using the specified
    cryptographic hash algorithm and a secret key.

    Parameters:
        algorithm_name (str): Name of the hash algorithm to use.
        message_data  (bytes): Raw data that needs to be signed.
        secret_key    (bytes): Key used for HMAC generation.

    Returns:
        bytes: The computed HMAC digest.

    Raises:
        ValueError: If the algorithm is unsupported or insecure.
    """
    # Validate algorithm name
    if algorithm_name not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure algorithm: {algorithm_name}. "
            f"Supported secure algorithms are: {', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Ensure the algorithm is available in hashlib
    try:
        hash_func = hashlib.new(algorithm_name)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not available.") from exc

    # Compute HMAC using the selected hash function
    hmac_obj = hmac.new(secret_key, message_data, digestmod=hash_func)
    return hmac_obj.digest()