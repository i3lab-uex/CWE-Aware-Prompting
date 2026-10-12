import hashlib
import hmac

# List of cryptographically secure hash algorithms supported by the standard library.
# Algorithms that are considered weak or deprecated (e.g., md5, sha1) are excluded.
_SECURE_HASH_ALGORITHMS = {
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
    # sha512_256 and sha512_224 are also considered secure, but some platforms may not
    # support them in the same way as the others. They can be added if required.
}

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The resulting HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or considered insecure.
    """
    if hash_algorithm_name.lower() not in _SECURE_HASH_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {hash_algorithm_name}"
        )

    # Secret key used for HMAC. In a real application this should be stored securely.
    secret_key = b"super_secret_key"

    # Create a new HMAC object using the chosen hash algorithm.
    hmac_obj = hmac.new(secret_key, payload, getattr(hashlib, hash_algorithm_name.lower()))
    return hmac_obj.digest()