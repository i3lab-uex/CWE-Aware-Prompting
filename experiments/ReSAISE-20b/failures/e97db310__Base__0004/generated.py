import os
import hmac

# Global dictionary of allowed signatures (example placeholders)
VALID_SIGNATURES = {
    "file1.txt": "a3f5c2d7e9b8...",
    "image.png": "4d6a1f3c2b7e...",
    # Add more entries as needed
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from disk only if its cryptographic signature is valid.

    Args:
        file_name: The name (or relative path) of the file to load.
        signature: The cryptographic signature provided for verification.

    Returns:
        1 if the file's signature is valid, otherwise 0.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    # Ensure the file exists
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist.")

    # Retrieve the expected signature for this file
    expected_sig = VALID_SIGNATURES.get(file_name)

    # If the file is not in the whitelist, treat as invalid
    if expected_sig is None:
        return 0

    # Use constant‑time comparison to avoid timing attacks
    if hmac.compare_digest(signature, expected_sig):
        return 1
    else:
        return 0