import hashlib
import hmac

# Define the set of cryptographically secure hash algorithms that are allowed.
_SECURE_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha512_256",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

def create_signature(algo_name: str, raw_data: bytes, secret_key: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given data using the specified
    hash algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hashing algorithm to use. Must be one of the secure algorithms.
    raw_data : bytes
        The data that will be signed.
    secret_key : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The generated signature (HMAC digest).

    Raises
    ------
    ValueError
        If an unsupported or insecure algorithm is requested.
    """
    algo_name = algo_name.lower()
    if algo_name not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm '{algo_name}'. "
            f"Allowed algorithms: {', '.join(sorted(_SECURE_ALGORITHMS))}"
        )

    # Create a new HMAC object with the chosen hash function.
    hmac_obj = hmac.new(secret_key, raw_data, digestmod=algo_name)
    return hmac_obj.digest()