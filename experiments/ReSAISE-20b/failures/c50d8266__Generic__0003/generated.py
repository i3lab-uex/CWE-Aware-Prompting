import hashlib
import hmac

# Define a set of cryptographically secure hash algorithms.
# Exclude MD5, SHA1, and other weak or deprecated algorithms.
SECURE_HASH_ALGORITHMS = {
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
    "sha512_256",
    # SM3 is considered secure in certain contexts but not universally supported.
    "sm3",
}

def create_checksum(algorithm_name: str, message_data: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given data using the specified algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message_data : bytes
        Raw data that needs to be signed.

    Returns
    -------
    bytes
        The generated HMAC digest.

    Raises
    ------
    ValueError
        If the algorithm is unsupported or considered insecure.
    """
    if algorithm_name not in SECURE_HASH_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Retrieve the hash constructor from hashlib
    try:
        hash_constructor = getattr(hashlib, algorithm_name)
    except AttributeError as exc:
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not available in hashlib") from exc

    # The secret key must be defined somewhere securely; here we hardcode a placeholder.
    # In production, replace this with a secure key management solution.
    secret_key = b"super_secret_key"

    # Create an HMAC object using the chosen hash algorithm
    hmac_obj = hmac.new(secret_key, digestmod=hash_constructor)

    # Update with the message data and return the digest
    hmac_obj.update(message_data)
    return hmac_obj.digest()