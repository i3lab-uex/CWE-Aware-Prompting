import hashlib
import hmac

# --- Global secret key for HMAC (in real code, keep this secure!) ---
SECRET_KEY = b"my_very_secret_key"

# --- Allowed hash algorithms (exclude insecure ones) ---
ALLOWED_ALGORITHMS = {
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

def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Create an HMAC signature of `payload` using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        Raw data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or considered insecure.
    """
    # Normalise algorithm name
    algo = algorithm_name.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm_name!r}. "
            f"Allowed algorithms are: {', '.join(sorted(ALLOWED_ALGORITHMS))}"
        )

    # Create HMAC object using the chosen hash algorithm
    h = hmac.new(SECRET_KEY, digestmod=hashlib.new(algo))

    # Feed the payload
    h.update(payload)

    return h.digest()