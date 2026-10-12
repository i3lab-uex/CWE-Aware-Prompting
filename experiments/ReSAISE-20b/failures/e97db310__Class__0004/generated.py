import os
import hmac

# Example global dictionary of allowed signatures.
# In a real system this would be populated securely from a trusted source.
VALID_SIGNATURES = {
    "example.txt": "5d41402abc4b2a76b9719d911017c592",
    "data.bin":   "e99a18c428cb38d5f260853678922e03",
    # Add more file:signature pairs as needed
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source after verifying its signature.

    Args:
        file_name: Name of the file to load.
        signature: Cryptographic signature supplied for verification.

    Returns:
        1 if the file's signature is valid, otherwise 0.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    # Ensure the file exists
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist")

    # Retrieve the expected signature for this file
    expected = VALID_SIGNATURES.get(file_name)
    if expected is None:
        # No known signature for this file; treat as invalid
        return 0

    # Perform a constant‑time comparison to mitigate timing attacks
    if hmac.compare_digest(signature, expected):
        return 1
    else:
        return 0