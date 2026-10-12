import os
import json
import hashlib

# Global dictionary mapping filenames to their expected SHA-256 signatures (hex strings)
TRUSTED_CONFIG_SIGNATURES = {
    # Example:
    # "config.json": "3a7bd3e2360a... (64 hex chars)",
}

def _compute_file_signature(file_path: str) -> str:
    """
    Compute the SHA-256 hash of a file's contents and return it as a hex string.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def validate_config_file(filename: str, cryptographic_signature: str):
    """
    Retrieve configuration data from a file and validate its cryptographic signature.

    Parameters
    ----------
    filename : str
        Name of the configuration file.
    cryptographic_signature : str
        The signature (hex string) sent with the configuration data.

    Returns
    -------
    dict or None
        The parsed configuration dictionary if the signature matches; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Ensure the file exists
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Verify the signature against the trusted list
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if not expected_sig:
        # No known signature for this file – treat as untrusted
        return None

    actual_sig = _compute_file_signature(filename)
    if actual_sig.lower() != expected_sig.lower():
        # Signature mismatch
        return None

    # Verify that the provided cryptographic_signature matches (extra safety check)
    if actual_sig.lower() != cryptographic_signature.lower():
        return None

    # Load and return the configuration data
    try:
        with open(filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        # If the file cannot be read or parsed, treat it as invalid
        return None

    if not isinstance(config_data, dict):
        # Configuration must be a dictionary
        return None

    return config_data