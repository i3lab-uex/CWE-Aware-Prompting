import hashlib
import hmac

# A global secret key used for HMAC signing.
# In real applications this should be stored securely (e.g., in a key vault).
secret_key: bytes = b"super_secret_key_used_for_hmac"

# Only cryptographically strong hash algorithms are allowed.
SECURE_HASH_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sm3",
    "sha3_224",
    "shake_128",
    "sha512",
    "sha512_224",
    "shake_256",
    "sha3_512",
    "blake2s",
    "sha3_384",
}


def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for the provided data using a specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (must be one of SECURE_HASH_ALGORITHMS).
    content : bytes
        The data to sign.

    Returns
    -------
    bytes
        The HMAC signature of the content.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or considered insecure.
    """
    # Normalise algorithm name
    alg = hash_algorithm.lower()
    if alg not in SECURE_HASH_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm}")

    # Create a new HMAC object with the chosen digest method
    try:
        hmac_obj = hmac.new(secret_key, content, digestmod=hashlib.new(alg))
    except ValueError as exc:
        # hashlib.new will raise ValueError if the algorithm name is invalid
        raise ValueError(f"Failed to create hash object for {hash_algorithm}") from exc

    return hmac_obj.digest()