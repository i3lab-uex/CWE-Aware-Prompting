import hashlib
import hmac

# Define a set of algorithms that are considered secure for HMAC usage.
SECURE_ALGORITHMS = {
    "sha256",
    "sha512",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

# Secret key used for HMAC signing. In a real application this should be
# stored securely (e.g., in an environment variable or secret manager).
secret_key = b"your-very-secure-secret-key"

def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the desired hash algorithm (e.g., "sha256", "blake2b").
    message : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or considered insecure.
    """
    # Normalize the algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm_name}. "
            "Supported algorithms are: " + ", ".join(sorted(SECURE_ALGORITHMS))
        )

    # Create a new hash object with the chosen algorithm
    try:
        hash_obj = hashlib.new(algo)
    except ValueError as exc:
        # This should not happen because we filter the list, but guard anyway
        raise ValueError(f"Hash algorithm {algorithm_name} is not available.") from exc

    # Compute HMAC using the secure hash object
    hmac_obj = hmac.new(secret_key, msg=message, digestmod=hash_obj)
    return hmac_obj.digest()