import hashlib
import hmac

# Define a whitelist of secure hash algorithms.
SECURE_HASHES = {
    "sha512_256",
    "sha224",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sm3",          # Assuming SM3 is considered secure in the target environment
    "sha3_224",
    "shake_128",
    "sha512",
    "sha512_224",
    "shake_256",
    "sha3_512",
    "blake2s",
    "sha3_384",
}

# A key used for HMAC signing. In a real application this should be
# securely stored and managed (e.g., using a secrets manager).
SECRET_KEY = b"super_secret_key"

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        The name of a supported hash algorithm (e.g., 'sha256', 'blake2b').
    content : bytes
        The data to sign.

    Returns
    -------
    bytes
        The HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or considered insecure.
    """
    # Normalise algorithm name to lower case for comparison
    algo = hash_algorithm.lower()

    if algo not in SECURE_HASHES:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm}")

    # Verify that the hashlib implementation supports the algorithm
    try:
        hash_func = hashlib.new(algo)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm not available in this environment: {hash_algorithm}") from exc

    # Compute HMAC using the selected hash function
    return hmac.new(SECRET_KEY, content, digestmod=hash_func).digest()