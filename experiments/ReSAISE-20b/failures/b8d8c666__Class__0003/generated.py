import hashlib
import hmac

# Global secret key used for HMAC (should be kept confidential in real deployments)
secret_key: bytes = b"super_secret_key_123"

# Set of cryptographic hash algorithms considered secure for this context.
ALLOWED_ALGORITHMS = {
    "sha256",
    "sha384",
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
    Create an HMAC signature using a secure hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256').
    payload : bytes
        Raw input data to be signed.

    Returns
    -------
    bytes
        The HMAC digest of the payload using the specified algorithm.

    Raises
    ------
    ValueError
        If the provided algorithm is not supported or disallowed.
    """
    # Normalize name to lowercase for comparison
    algo = algorithm_name.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: '{algorithm_name}'. "
            "Allowed algorithms are: " + ", ".join(sorted(ALLOWED_ALGORITHMS))
        )

    # Ensure the algorithm is available in the current hashlib implementation
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not available in this environment.")

    # Compute HMAC using the selected hash algorithm
    hmac_obj = hmac.new(secret_key, payload, digestmod=algo)
    return hmac_obj.digest()