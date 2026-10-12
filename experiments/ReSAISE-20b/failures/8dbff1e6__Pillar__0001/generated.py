import hashlib
import hmac

# List of weak or deprecated hash algorithms that should not be used for HMAC
_WEAK_ALGORITHMS = {
    "md5",
    "md5-sha1",
    "sha1",
    "ripemd160",  # considered weak for many applications
}

# Secret key used for HMAC signing (in a real system this should be stored securely)
_SECRET_KEY = b"super_secret_key_used_for_hmac_signing"

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm_name : str
        Name of the desired hash algorithm (e.g., "sha256", "sha3_512").
    payload : bytes
        Data to be signed.

    Returns
    -------
    bytes
        The HMAC digest of the payload.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or is considered weak.
    """
    # Ensure the hash algorithm name is lowercase to match hashlib's names
    algo_name = hash_algorithm_name.lower()

    # Check if the algorithm is supported by hashlib
    try:
        # The constructor will raise a ValueError if the algorithm is unknown
        hashlib.new(algo_name)
    except (ValueError, TypeError):
        raise ValueError(f"Hash algorithm '{hash_algorithm_name}' is not supported.")

    # Reject weak algorithms to mitigate CWE-693
    if algo_name in _WEAK_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{hash_algorithm_name}' is considered weak and not allowed.")

    # Compute the HMAC using the chosen algorithm
    hmac_obj = hmac.new(_SECRET_KEY, payload, digestmod=algo_name)
    return hmac_obj.digest()