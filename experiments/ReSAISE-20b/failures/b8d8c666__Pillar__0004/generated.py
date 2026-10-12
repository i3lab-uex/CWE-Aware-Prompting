import hashlib
import hmac

# Define a secret key for HMAC (in practice this should be stored securely)
SECRET_KEY = b"super_secret_key_used_for_hmac_signatures"

# Set of hash algorithms that are considered secure for HMAC usage
ALLOWED_ALGORITHMS = {
    "sha256",
    "sha384",
    "sha512",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    # SHA-512/256 is a truncated variant of SHA‑512 and still considered secure
    "sha512_256",
    # SM3 is a Chinese standard hash function, included here for completeness
    "sm3",
}

def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Create an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256').
    payload : bytes
        The raw data to sign.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested algorithm is not in the list of allowed algorithms.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algorithm_name}")

    # Create a new HMAC object with the chosen hash constructor
    try:
        hmac_obj = hmac.new(SECRET_KEY, payload, digestmod=hashlib.new(algo))
    except ValueError as exc:
        # This captures errors from hashlib when the algorithm name is invalid
        raise ValueError(f"Invalid hash algorithm specified: {algorithm_name}") from exc

    return hmac_obj.digest()