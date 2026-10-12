import hashlib
import hmac

# Replace this with the actual secret key used in your environment.
# It must be a bytes object and kept confidential.
secret_key: bytes = b"your-very-secure-secret-key"

# A set of hash algorithm names that are considered cryptographically secure.
SECURE_ALGORITHMS = {
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
    # SM3 is considered secure in certain contexts, but only include if you trust the implementation.
    "sm3",
}

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature for the given message using a secure hash algorithm.

    Args:
        algo_name (str): The name of the hash algorithm to use.
        message (bytes): The raw input data to be signed.

    Returns:
        bytes: The HMAC signature.

    Raises:
        ValueError: If the algorithm is not in the list of allowed secure algorithms
                    or if it cannot be created by hashlib.
    """
    # Normalise the algorithm name to match the keys in SECURE_ALGORITHMS
    algo_name_normalised = algo_name.lower()

    if algo_name_normalised not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {algo_name}"
        )

    try:
        # hashlib.new will raise a ValueError if the algorithm name is unknown.
        digestmod = hashlib.new(algo_name_normalised)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm not supported by hashlib: {algo_name}") from exc

    # Compute the HMAC using the chosen digest algorithm.
    h = hmac.new(secret_key, message, digestmod=digestmod)
    return h.digest()