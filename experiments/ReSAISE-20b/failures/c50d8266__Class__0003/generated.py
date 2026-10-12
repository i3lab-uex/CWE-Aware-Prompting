import hashlib
import hmac

# List of algorithms that are considered secure for this context.
SECURE_ALGORITHMS = {
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
    "ripemd160",      # widely used and considered secure
    "sm3",            # Chinese national standard, accepted as secure in many contexts
}

def create_checksum(algorithm_name: str, message_data: bytes, secret_key: bytes) -> bytes:
    """
    Generate a cryptographic signature for the given message using HMAC.

    Parameters
    ----------
    algorithm_name : str
        Name of the hashing algorithm to use (e.g., 'sha256', 'blake2b').
    message_data : bytes
        Raw data that needs to be signed.
    secret_key : bytes
        Secret key used in the HMAC construction.

    Returns
    -------
    bytes
        The generated signature (HMAC digest).

    Raises
    ------
    ValueError
        If the requested algorithm is not available or is considered insecure.
    """
    # Normalise algorithm name (hashlib is case‑insensitive but we store lower‑case)
    algo = algorithm_name.lower()

    # Verify that the algorithm exists in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algorithm_name}' is not available.")

    # Reject insecure or deprecated algorithms
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' is considered insecure and cannot be used.")

    # Construct HMAC using the chosen hash function
    h = hmac.new(secret_key, message_data, digestmod=hashlib.new(algo))
    return h.digest()