import hashlib
import hmac

# A set of hash algorithms that are considered secure for HMAC usage.
SECURE_HASHES = {
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
    # SHA-512/256 is a truncated version of SHA-512, still secure.
    "sha512_256",
}

def create_checksum(
    algorithm_name: str,
    message_data: bytes,
    secret_key: bytes = b"default_secret_key",
) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given message data using
    the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hashing algorithm to use. Must be one of the secure
        algorithms listed in SECURE_HASHES.
    message_data : bytes
        Raw data that needs to be signed.
    secret_key : bytes, optional
        Key used for HMAC. Defaults to a static key if not provided.

    Returns
    -------
    bytes
        The generated HMAC signature.

    Raises
    ------
    ValueError
        If the specified algorithm is unsupported or insecure.
    """
    # Normalize algorithm name to match hashlib names
    algo = algorithm_name.lower()

    if algo not in SECURE_HASHES:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm_name!r}. "
            "Only secure algorithms are allowed."
        )

    # Verify that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm {algorithm_name!r} is not available in hashlib.")

    # Compute the HMAC signature
    hmac_obj = hmac.new(secret_key, message_data, digestmod=algo)
    return hmac_obj.digest()