import os
import hmac

# Example global dictionary of allowed signatures (hashes)
VALID_SIGNATURES = {
    # 'filename': 'hex_digest',
    # e.g. 'example.txt': 'a3b2c1...',
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source after verifying its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the file to be loaded.
    signature : str
        Hexadecimal representation of the cryptographic signature for the file.

    Returns
    -------
    int
        1 if the signature is valid and the file exists, otherwise 0.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist on disk.
    """
    # Check existence first to avoid leaking information about missing files
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist.")

    # Retrieve the expected signature for this file
    expected_sig = VALID_SIGNATURES.get(file_name)
    if expected_sig is None:
        # File not in the whitelist
        return 0

    # Use constant‑time comparison to mitigate timing attacks
    if hmac.compare_digest(expected_sig.lower(), signature.lower()):
        return 1

    return 0