import os
import hashlib
import json

# Global dictionary mapping filenames to their trusted SHA‑256 signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (populate with real values in production)
    "app_config.json": "5e884898da28047151d0e56f8dc6292773603d0d6aabbddc...",
    "db_config.yaml":  "2c26b46b68ffc68ff99b453c1d3041341345f8f9e7a2..."
}

def _compute_file_signature(filepath: str) -> str:
    """
    Compute the SHA‑256 hexadecimal digest of a file's contents.
    Reads the file in binary mode to support arbitrary data types.
    """
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from a file after verifying its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    crypt_signature : str
        Signature that was sent alongside the configuration data.

    Returns
    -------
    dict | None
        Parsed JSON configuration if signature matches; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file does not exist.
    """
    # Ensure the file exists
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist")

    # Verify that the supplied signature matches the trusted one
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if trusted_sig is None:
        # No known signature for this file – treat as untrusted
        return None

    # Compute the actual signature of the file contents
    try:
        actual_sig = _compute_file_signature(config_filename)
    except Exception as e:
        # Any error reading the file is treated as a failure to verify
        return None

    # Constant‑time comparison to mitigate timing attacks
    if not hashlib.compare_digest(actual_sig, trusted_sig):
        return None

    # Verify that the supplied cryptographic signature matches the computed one
    if not hashlib.compare_digest(crypt_signature, actual_sig):
        return None

    # Load the configuration data (JSON assumed; adjust if needed)
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Malformed JSON or read error – treat as invalid
        return None