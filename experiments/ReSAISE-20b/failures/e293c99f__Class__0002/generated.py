import hashlib
import hmac

# Example secret key – in practice this should be securely generated and stored.
SECRET_KEY = b"super_secret_key"

# Set of cryptographically secure hash algorithms supported by this function.
SECURE_ALGORITHMS = {
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    "sha512_256",
    # Include SM3 if your platform supports it and you trust its security.
    "sm3",
}


def create_signature(algo_name: str, raw_data: bytes) -> bytes:
    """
    Generate a cryptographic signature for the given data using HMAC with the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hashing algorithm to use. Must be one of the secure algorithms listed in SECURE_ALGORITHMS.
    raw_data : bytes
        The data to sign.

    Returns
    -------
    bytes
        HMAC signature of the data.

    Raises
    ------
    ValueError
        If an unsupported or insecure hash algorithm is specified.
    """
    algo_name_lower = algo_name.lower()

    # Verify that the requested algorithm is both available and considered secure.
    if (
        algo_name_lower not in SECURE_ALGORITHMS
        or algo_name_lower not in hashlib.algorithms_available
    ):
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algo_name}. "
            "Allowed algorithms are: "
            f"{', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Create HMAC using the chosen algorithm.
    hmac_obj = hmac.new(SECRET_KEY, raw_data, digestmod=algo_name_lower)
    return hmac_obj.digest()