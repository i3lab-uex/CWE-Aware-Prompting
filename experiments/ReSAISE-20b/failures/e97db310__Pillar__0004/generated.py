import os
from pathlib import Path
import hmac

# Example global dictionary of allowed file signatures.
# In a real application this should be populated securely from a trusted source.
VALID_SIGNATURES = {
    "file1.txt": "a3f5c8e9d0b7...",
    "image.png": "b1c2d3e4f5a6..."
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source after validating its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the file to load. Must be a relative path only (no directory traversal).
    signature : str
        Cryptographic signature provided for the file.

    Returns
    -------
    int
        1 if the signature is valid, otherwise 0.

    Raises
    ------
    FileNotFoundError
        If the file does not exist or the path attempts directory traversal.
    """
    # Prevent directory traversal by rejecting absolute paths and any parent references
    path = Path(file_name).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"File '{file_name}' does not exist or is not a regular file.")

    # Use constant‑time comparison to avoid timing attacks
    expected_sig = VALID_SIGNATURES.get(file_name)
    if expected_sig is None:
        return 0

    # hmac.compare_digest ensures constant‑time comparison
    if not hmac.compare_digest(signature, expected_sig):
        return 0

    # Here you would actually load or process the file as needed.
    # For this exercise we simply return success.
    return 1