import hashlib
import hmac

# Secure hash algorithms that are considered safe for cryptographic purposes.
ALLOWED_ALGORITHMS = {
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
    # SM3 is considered secure in many contexts, but its support depends on the
    # OpenSSL/cryptography backend. It is included here for completeness.
    "sm3",
}

def create_checksum(
    algorithm_name: str,
    message_data: bytes,
    secret_key: bytes
) -> bytes:
    """
    Generate a cryptographic signature for `message_data` using the specified
    hash algorithm and HMAC with the provided secret key.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256').
    message_data : bytes
        Raw data that needs to be signed.
    secret_key : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The generated HMAC signature.

    Raises
    ------
    ValueError
        If `algorithm_name` is not in the list of allowed secure algorithms.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm_name!r}"
        )

    # Ensure the backend supports the chosen algorithm
    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"The selected algorithm {algorithm_name!r} is not available in this environment."
        )

    # Create the HMAC object using the chosen hash function
    hmac_obj = hmac.new(secret_key, message_data, digestmod=algo)

    # Return the binary signature
    return hmac_obj.digest()