import os

# Global dictionary containing allowed file signatures.
# Keys are file names and values are the expected cryptographic signatures (hex strings).
VALID_SIGNATURES = {
    # Example entries – replace with real values in production.
    "example.txt": "a1b2c3d4e5f6g7h8i9j0",
    "data.bin":   "0123456789abcdef0123"
}

def load_file(file_name: str, signature: str) -> int:
    """
    Load a file from a third‑party source after verifying its signature.

    Parameters
    ----------
    file_name : str
        Name of the file to be loaded.
    signature : str
        Cryptographic signature (hex string) that must match the one stored in VALID_SIGNATURES.

    Returns
    -------
    int
        1 if the signature is valid, else 0.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    """
    # Check that the file exists before performing any further checks.
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' does not exist.")

    # Retrieve the expected signature for this file from the global dictionary.
    expected_sig = VALID_SIGNATURES.get(file_name)

    # If we have no entry for the file, treat it as invalid.
    if expected_sig is None:
        return 0

    # Compare the provided signature with the expected one in a constant‑time manner.
    # Using Python's built‑in `hmac.compare_digest` helps mitigate timing attacks.
    import hmac
    if isinstance(signature, str):
        signature_bytes = signature.encode('utf-8')
    else:
        signature_bytes = signature

    if isinstance(expected_sig, str):
        expected_bytes = expected_sig.encode('utf-8')
    else:
        expected_bytes = expected_sig

    if hmac.compare_digest(signature_bytes, expected_bytes):
        return 1
    else:
        return 0