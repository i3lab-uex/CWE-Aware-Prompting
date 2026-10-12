import hashlib
import hmac

# Define the secret key that will be used for HMAC signatures.
# In a real application this should be securely stored and managed.
secret_key: bytes = b"my-very-secret-key"

# Set of hash algorithms that are considered secure for HMAC usage.
ALLOWED_ALGORITHMS = {
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
    # The following are considered acceptable for HMAC in many contexts
    "sha512_256",
}

def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Create an HMAC cryptographic signature for the given payload using
    the specified hash algorithm.

    Parameters:
        algorithm_name (str): The name of the hash algorithm to use.
        payload (bytes): The raw input data to be signed.

    Returns:
        bytes: The computed HMAC signature.

    Raises:
        ValueError: If the algorithm is unsupported or disallowed.
    """
    # Normalise the algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {algorithm_name}"
        )

    # Ensure the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not available in this Python build.")

    # Create the HMAC object and compute the signature
    hmac_obj = hmac.new(secret_key, payload, digestmod=algo)
    return hmac_obj.digest()