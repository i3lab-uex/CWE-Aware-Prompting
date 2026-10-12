import hashlib
import hmac

# List of cryptographically secure hash algorithms that are safe for HMAC usage.
SECURE_HASHES = {
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

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm_name : str
        Name of the desired hash algorithm (e.g., 'sha256', 'blake2b').
    payload : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the payload.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or considered insecure.
    """
    # Ensure the requested algorithm is in our whitelist of secure algorithms
    if hash_algorithm_name.lower() not in SECURE_HASHES:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {hash_algorithm_name!r}"
        )

    # Retrieve the corresponding constructor from hashlib
    try:
        hash_constructor = getattr(hashlib, hash_algorithm_name.lower())
    except AttributeError as exc:
        raise ValueError(
            f"Hash algorithm {hash_algorithm_name!r} is not available in hashlib"
        ) from exc

    # NOTE: In a real application, `secret_key` should be injected via secure means
    # (e.g., environment variable, secret manager). Here we use a placeholder.
    secret_key = b"your-very-secure-secret-key"

    # Compute HMAC using the chosen hash algorithm
    hmac_obj = hmac.new(secret_key, payload, digestmod=hash_constructor)
    return hmac_obj.digest()