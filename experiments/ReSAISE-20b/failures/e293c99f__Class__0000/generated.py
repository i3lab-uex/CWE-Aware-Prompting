import hashlib
import hmac

# List of cryptographic hash algorithms considered secure for HMAC usage.
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
    # SM3 is considered secure in some jurisdictions; include if desired.
    "sm3",
}

# A global secret key used for generating signatures. In a real-world scenario,
# this should be stored securely (e.g., in an HSM or protected key store).
SECRET_KEY = b"my_very_secret_key_that_should_be_long_and_random"

def create_signature(algo_name: str, raw_data: bytes) -> bytes:
    """
    Generate an HMAC-based cryptographic signature for the given data using
    a specified hash algorithm.

    Parameters:
        algo_name (str): Name of the hashing algorithm to use.
        raw_data (bytes): The data that needs to be signed.

    Returns:
        bytes: The HMAC digest (signature).

    Raises:
        ValueError: If the specified algorithm is not supported or considered insecure.
    """
    # Normalize algorithm name to lower case for comparison
    algo_name = algo_name.lower()

    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algo_name}. "
            "Supported algorithms are: " + ", ".join(sorted(SECURE_ALGORITHMS))
        )

    # Create an HMAC object with the chosen digest mode
    hmac_obj = hmac.new(SECRET_KEY, raw_data, digestmod=algo_name)
    return hmac_obj.digest()