import os
from pathlib import Path

# Global dictionary of allowed signatures
VALID_SIGNATURES = {
    # Example entries – replace with real values in production
    "example.txt": "a1b2c3d4e5f6g7h8i9j0",
    "config.yaml": "1234567890abcdef",
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source after validating its cryptographic signature.

    Parameters
    ----------
    file_name : str
        The name (or path) of the file to be loaded.
    signature : str
        The cryptographic signature provided for this file.

    Returns
    -------
    int
        1 if the signature is valid, otherwise 0.

    Raises
    ------
    FileNotFoundError
        If the file does not exist on disk.
    """
    # Resolve to an absolute path to avoid relative traversal tricks
    file_path = Path(file_name).resolve()

    # Check that the file exists; raise FileNotFoundError if it does not
    if not file_path.is_file():
        raise FileNotFoundError(f"File '{file_name}' does not exist.")

    # Validate the signature against the allowed list
    expected_sig = VALID_SIGNATURES.get(file_path.name)
    if expected_sig is None:
        # No signature registered for this file
        return 0

    return 1 if signature == expected_sig else 0