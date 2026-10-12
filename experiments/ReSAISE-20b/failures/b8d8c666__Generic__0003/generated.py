import hashlib
import hmac

# Global secret key used for HMAC signing (should be kept secret!)
secret_key: bytes = b"super-secret-key-that-is-32-bytes!"

# Set of hash algorithms considered secure for this application
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
}

def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Create an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    payload : bytes
        Raw data to sign.

    Returns
    -------
    bytes
        HMAC digest of the payload.

    Raises
    ------
    ValueError
        If the requested algorithm is not in the list of secure algorithms or
        if it is not available on this platform.
    """
    # Normalize the algorithm name (hashlib uses lower‑case names)
    alg = algorithm_name.lower()

    # Check that the requested algorithm is permitted
    if alg not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algorithm_name}' is disallowed or unsupported.")

    # Ensure the algorithm is actually available in hashlib
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algorithm_name}' is not available on this system.")

    # Compute the HMAC using the chosen hash algorithm
    hmac_obj = hmac.new(secret_key, payload, digestmod=alg)
    return hmac_obj.digest()