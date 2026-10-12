import json
import os
from typing import Dict, Any

# Example trusted signatures mapping.
# In a real application this would be populated from a secure source
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    "config.json": "d41d8cd98f00b204e9800998ecf8427e",
    # add other trusted filenames and their signatures here
}


def _compute_file_signature(file_path: str) -> str:
    """
    Compute the MD5 hex digest of the file contents.
    This is a simple placeholder; in production you would use a stronger
    hash algorithm (e.g., SHA-256) and a proper key‑based signature scheme.
    """
    import hashlib
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def retrieve_config_data(config_filename: str, crypt_signature: str) -> Dict[str, Any] | None:
    """
    Retrieve configuration data from *config_filename* and verify its cryptographic
    signature against the trusted signatures dictionary.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to load.
    crypt_signature : str
        The cryptographic signature provided for verification.

    Returns
    -------
    dict | None
        The parsed configuration data if the signature matches; otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be read.
    """
    # Ensure the file exists
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist")

    # Compute the actual signature of the file
    try:
        actual_signature = _compute_file_signature(config_filename)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to compute signature for '{config_filename}': {exc}") from exc

    # Validate the provided signature
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(os.path.basename(config_filename))
    if expected_signature is None:
        # If we have no record of this file, treat it as untrusted
        return None

    if crypt_signature != expected_signature or actual_signature != expected_signature:
        # Signature mismatch
        return None

    # Load and parse the configuration file (JSON assumed)
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read or parse '{config_filename}': {exc}") from exc

    return config_data