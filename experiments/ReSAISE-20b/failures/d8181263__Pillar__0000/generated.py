import hashlib
import hmac

# List of hash algorithms that are considered secure for HMAC usage.
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
}

# Mapping from algorithm name to the constructor in hashlib.
_HASH_ALGORITHMS = {
    name: getattr(hashlib, name) for name in SECURE_HASHES
}

def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for *message* using the specified hash *algorithm*.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        Raw data that needs to be signed.

    Returns
    -------
    bytes
        The HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If *algorithm* is not supported or considered insecure.
    """
    if algorithm.lower() not in SECURE_HASHES:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm}")

    # In a real-world scenario the secret key would come from a secure source.
    # For this example we use a fixed key, but in production it should be
    # stored securely (e.g., hardware security module or environment variable).
    secret_key = b"super_secret_key"

    # Create an HMAC object using the chosen hash constructor.
    hmac_obj = hmac.new(secret_key, message, _HASH_ALGORITHMS[algorithm.lower()])

    return hmac_obj.digest()