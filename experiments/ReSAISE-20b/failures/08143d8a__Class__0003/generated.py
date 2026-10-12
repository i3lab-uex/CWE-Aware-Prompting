import json
import os
import hashlib

# Global mapping of trusted signatures to config file names.
# Example: {"a3f1...": "app_config.json", ...}
TRUSTED_CONFIG_SIGNATURES = {
    # Populate with actual trusted signatures.
}

def _compute_file_hash(file_path: str) -> str:
    """Return the SHA‑256 hex digest of the file contents."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()

def evaluate_config_file(config_filename: str, provided_sig: str):
    """
    Load a configuration file only if its cryptographic signature is valid.

    Parameters
    ----------
    config_filename : str
        The name of the configuration file to load.
    provided_sig : str
        The cryptographic signature supplied with the configuration data.

    Returns
    -------
    dict | None
        The parsed JSON content of the file if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be read.
    """
    # Ensure the requested file exists
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' not found")

    # Verify the provided signature is in the trusted list
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(provided_sig)
    if expected_file != config_filename:
        # Either the signature is unknown or does not match this file
        return None

    # Compute the hash of the actual file contents to guard against tampering
    computed_hash = _compute_file_hash(config_filename)
    if computed_hash != provided_sig:
        # The content does not match the supplied signature
        return None

    # Load and parse the configuration (JSON format assumed)
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # Any parsing or IO error results in an IOError
        raise IOError(f"Failed to read configuration file '{config_filename}': {e}") from e