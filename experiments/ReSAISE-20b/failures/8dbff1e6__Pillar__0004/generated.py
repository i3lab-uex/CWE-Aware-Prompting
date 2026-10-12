import os
import hashlib
import hmac

# A secret key used for HMAC signing.
# In a real system this should be stored securely (e.g. environment variable,
# secret manager, etc.) and kept out of source control.
SECRET_KEY = os.getenv("HMAC_SECRET_KEY", "default-secret").encode()

# Secure hash algorithms that are considered safe for HMAC usage.
SECURE_HASH_ALGORITHMS = {
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

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        Data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or considered insecure.
    """
    # Normalize the algorithm name to lower case
    algo = hash_algorithm_name.lower()

    if algo not in SECURE_HASH_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {hash_algorithm_name}"
        )

    # The `hmac.new` function accepts a callable or a string name for the digestmod.
    # Using the algorithm name directly ensures compatibility with hashlib.
    try:
        signature = hmac.new(SECRET_KEY, payload, digestmod=algo).digest()
    except Exception as exc:
        # This should not happen for supported algorithms, but we guard against
        # unexpected failures and raise a generic ValueError.
        raise ValueError(f"Failed to generate HMAC: {exc}") from exc

    return signature