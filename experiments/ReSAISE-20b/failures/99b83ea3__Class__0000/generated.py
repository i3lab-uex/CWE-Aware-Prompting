import hashlib
import hmac

# Define a set of secure hash algorithms that are safe for HMAC usage.
SECURE_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    "sha512_224",
    "sha512_256",
}

def create_signature(algorithm_name: str, message: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use. Must be one of the secure algorithms defined in SECURE_ALGORITHMS.
    message : bytes
        The data to be signed.
    secret_key : bytes
        Key used for the HMAC signing procedure.

    Returns
    -------
    bytes
        The computed signature (HMAC digest).

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or considered insecure.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # hashlib.new accepts the algorithm name directly
    try:
        hash_func = hashlib.new(algo)
    except ValueError as exc:
        # In case the algorithm is present in hashlib but not suitable for HMAC
        raise ValueError(f"Hash algorithm {algorithm_name} is unavailable") from exc

    # Compute HMAC using the selected hash function
    return hmac.new(secret_key, message, digestmod=hash_func).digest()