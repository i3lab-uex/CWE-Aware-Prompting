import os
import hmac

# Example global dictionary of allowed signatures.
# In a real application this would be securely loaded from a trusted source.
VALID_SIGNATURES = {
    "example.txt": "d2b9f3c4e5a6b7c8d9e0f1a2b3c4d5e6",
    "data.bin":   "abcdef1234567890fedcba0987654321",
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source after verifying its cryptographic signature.

    Parameters
    ----------
    file_name : str
        The name of the file to load.
    signature : str
        The cryptographic signature provided for the file.

    Returns
    -------
    int
        1 if the signature is valid, 0 otherwise.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    # Ensure the file exists before attempting to read it
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist")

    # Retrieve the expected signature for this file
    expected_sig = VALID_SIGNATURES.get(file_name)

    # If we have no record of this file, reject it
    if expected_sig is None:
        return 0

    # Use a constant‑time comparison to avoid timing attacks
    if hmac.compare_digest(signature, expected_sig):
        return 1

    return 0