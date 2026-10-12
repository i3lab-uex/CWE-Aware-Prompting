import hashlib
import hmac

# Define a whitelist of cryptographically secure hash algorithms.
# Only SHA‑2, SHA‑3 and BLAKE2 families are allowed.
_SECURE_ALGORITHMS = {
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

# A secret key used for HMAC. In a real application this would be securely stored.
_SECRET_KEY = b"super-secret-key"

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        The raw input data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested algorithm is not in the whitelist of secure algorithms.
    """
    # Normalise algorithm name to lowercase
    algo_name = algo_name.lower()

    if algo_name not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {algo_name!r}. "
            f"Allowed algorithms are: {sorted(_SECURE_ALGORITHMS)}"
        )

    # Create a new hash object using the selected algorithm
    hash_func = hashlib.new(algo_name)

    # Compute HMAC using the secret key and the chosen hash function
    hmac_obj = hmac.new(_SECRET_KEY, msg=message, digestmod=hash_func)
    return hmac_obj.digest()