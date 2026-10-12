import json
import os
import hmac
import hashlib

# Example trusted signatures mapping: filename -> expected hex digest
TRUSTED_CONFIG_SIGNATURES = {
    "config.json": "d2c6e7b1a8f3c9e4b5a6d7f8c9e0f1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8",
    # Add more trusted signatures here
}


def _compute_file_digest(filepath: str) -> str:
    """
    Compute the SHA-256 hex digest of a file in a memory‑efficient way.
    """
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def validate_config_file(filename: str, cryptographic_signature: str):
    """
    Validate the configuration file against its cryptographic signature.

    Parameters
    ----------
    filename : str
        Path to the configuration file.
    cryptographic_signature : str
        Hexadecimal representation of the expected SHA‑256 signature.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature matches; otherwise None.

    Raises
    ------
    IOError
        If the file does not exist or cannot be opened.
    """
    # Ensure the file exists
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Compute the actual digest of the file
    try:
        actual_digest = _compute_file_digest(filename)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Error reading configuration file '{filename}': {exc}") from exc

    # If a trusted signature is known for this file, use it as the expected value
    expected_digest = TRUSTED_CONFIG_SIGNATURES.get(filename, cryptographic_signature)

    # Perform a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(actual_digest, expected_digest):
        return None

    # Parse the configuration data (assumed to be JSON)
    try:
        with open(filename, "r", encoding="utf-8") as fh:
            config_data = json.load(fh)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Error parsing configuration file '{filename}': {exc}") from exc

    return config_data