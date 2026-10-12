import hashlib
import hmac

# Secret key used for HMAC signing (must be kept confidential)
secret_key: bytes = b'super_secret_key'

# A whitelist of cryptographic hash algorithms considered secure for HMAC
_SECURE_ALGORITHMS = {
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

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate an HMAC signature for the given payload using a specified hash algorithm.

    Parameters
    ----------
    hash_algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        Data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the payload.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or considered insecure.
    """
    # Normalise the algorithm name (hashlib uses lowercase names)
    algo_name = hash_algorithm_name.lower()

    # Reject unsupported or insecure algorithms
    if algo_name not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Hash algorithm '{hash_algorithm_name}' is not supported or "
            "considered insecure. Supported algorithms: "
            f"{', '.join(sorted(_SECURE_ALGORITHMS))}"
        )

    # Verify that the algorithm is actually available in hashlib
    try:
        hash_func = hashlib.new(algo_name)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm '{hash_algorithm_name}' is not available.") from exc

    # Compute HMAC
    hmac_obj = hmac.new(secret_key, payload, digestmod=hash_func)
    return hmac_obj.digest()