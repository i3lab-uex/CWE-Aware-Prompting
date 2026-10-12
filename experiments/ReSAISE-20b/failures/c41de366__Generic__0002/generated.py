import json
import os
import hashlib
from typing import Dict, Any

# Example trusted signatures mapping.
# In a real system this would be securely stored and managed.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    "config.json": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd9c5b4e7c6f2f8d1ea",
    # Add more file:signature pairs as needed
}

def _compute_file_hash(file_path: str) -> str:
    """
    Compute the SHA256 hash of a file's contents.
    """
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def retrieve_config_data(config_filename: str, crypt_signature: str) -> Dict[str, Any] | None:
    """
    Retrieve configuration data from an external file after verifying its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        The name of the file containing the configuration data.
    crypt_signature : str
        The cryptographic signature sent with the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Ensure the file exists
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist.")

    # Compute the SHA256 hash of the file
    actual_hash = _compute_file_hash(config_filename)

    # Compare with the provided signature (case-insensitive)
    if actual_hash.lower() != crypt_signature.lower():
        # Signature mismatch – do not load the config
        return None

    # Load and parse JSON configuration safely
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        # If JSON is malformed or file cannot be read, treat as invalid
        return None

    if not isinstance(config_data, dict):
        # Expecting a dictionary; otherwise invalid
        return None

    return config_data