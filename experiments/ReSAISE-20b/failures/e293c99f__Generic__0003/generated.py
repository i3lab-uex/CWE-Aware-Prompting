import hashlib
import hmac

# Secret key used for signing (must be defined elsewhere in the application)
# For example:
# secret_key = b'super_secret_key'

# List of cryptographic hash algorithms considered secure
SECURE_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha512_256',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
}

def create_signature(algo_name: str, raw_data: bytes) -> bytes:
    """
    Generate an HMAC-based cryptographic signature for the given data.

    Parameters
    ----------
    algo_name : str
        Name of the hashing algorithm to use (e.g., 'sha256').
    raw_data : bytes
        Raw data that needs to be signed.

    Returns
    -------
    bytes
        The generated signature (HMAC digest).

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or considered insecure.
    """
    # Validate algorithm name (case-insensitive)
    algo_name_lower = algo_name.lower()
    if algo_name_lower not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure algorithm '{algo_name}'. "
            f"Supported algorithms: {sorted(SECURE_ALGORITHMS)}"
        )

    # Ensure the algorithm is available in hashlib
    if algo_name_lower not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_name}' is not available on this system.")

    # Compute HMAC signature
    try:
        return hmac.new(secret_key, raw_data, algo_name_lower).digest()
    except Exception as exc:
        raise ValueError(f"Failed to create signature: {exc}") from exc