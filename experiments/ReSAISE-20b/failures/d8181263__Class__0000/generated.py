import hashlib
import hmac

# Define the set of cryptographically secure hash algorithms that are allowed.
ALLOWED_ALGORITHMS = {
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

def sign_data(algorithm: str, message: bytes, secret_key: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given message using
    a secure hash algorithm.

    Parameters
    ----------
    algorithm : str
        The name of the hashing algorithm to use. Must be one of the
        algorithms listed in ALLOWED_ALGORITHMS.
    message : bytes
        The raw data to be signed.
    secret_key : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If an unsupported or insecure hash algorithm is specified.
    """
    # Ensure the algorithm name is in a canonical form (lowercase).
    algo_name = algorithm.lower()

    if algo_name not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm '{algorithm}'. "
            f"Allowed algorithms: {', '.join(sorted(ALLOWED_ALGORITHMS))}"
        )

    # Create a new hash object for the selected algorithm.
    try:
        hash_func = hashlib.new(algo_name)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm '{algorithm}' is not available.") from exc

    # Compute the HMAC using the provided secret key.
    return hmac.new(secret_key, message, digestmod=hash_func).digest()