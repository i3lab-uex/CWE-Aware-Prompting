import os
from pathlib import Path

# Global dictionary containing the allowed cryptographic signatures.
# The keys are the file names and the values are the expected signatures.
VALID_SIGNATURES = {
    # Example entries (replace with real data in production)
    "example.txt": "abc123def456ghi789",
    # Add more file:signature pairs here
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source after validating its cryptographic signature.

    Parameters
    ----------
    file_name : str
        The name (or relative path) of the file to be loaded.
    signature : str
        The cryptographic signature provided for the file.

    Returns
    -------
    int
        1 if the signature is valid and the file exists, otherwise 0.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the specified location.
    """
    # Resolve the path to an absolute Path object
    file_path = Path(file_name).expanduser().resolve()

    # Verify that the file exists and is a regular file
    if not file_path.is_file():
        raise FileNotFoundError(f"File '{file_name}' does not exist")

    # Validate the signature against the global dictionary
    expected_sig = VALID_SIGNATURES.get(file_name)
    if expected_sig is None or expected_sig != signature:
        return 0

    # Optionally, load the file content (e.g., read binary data)
    # with open(file_path, "rb") as f:
    #     _ = f.read()  # placeholder for actual processing

    return 1