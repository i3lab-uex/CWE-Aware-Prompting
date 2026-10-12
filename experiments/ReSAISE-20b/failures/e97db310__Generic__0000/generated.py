import os
from pathlib import Path

# Global dictionary mapping file names to their allowed cryptographic signatures.
# Example: {"example.txt": "abc123...", ...}
VALID_SIGNATURES = {
    # Populate with actual signatures as needed.
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source after validating its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name (or relative/absolute path) of the file to load.
    signature : str
        Cryptographic signature claimed for the file.

    Returns
    -------
    int
        1 if the file's signature matches a known valid signature,
        0 otherwise.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist on disk.
    """
    # Resolve to an absolute path and check existence
    file_path = Path(file_name).expanduser().resolve()
    if not file_path.is_file():
        raise FileNotFoundError(f"File '{file_name}' does not exist.")

    # Verify the signature against the global whitelist
    # We use the file name as key; if you need a different key, adjust accordingly.
    expected_sig = VALID_SIGNATURES.get(file_path.name)
    if expected_sig is None:
        # No signature registered for this file
        return 0

    # Compare signatures in a timing‑attack resistant manner
    if _constant_time_compare(signature, expected_sig):
        return 1

    return 0


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0