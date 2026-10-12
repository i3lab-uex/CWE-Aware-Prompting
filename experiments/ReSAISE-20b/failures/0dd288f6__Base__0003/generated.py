import os
import json
import hashlib
import hmac

# Example trusted signatures mapping (filename -> expected SHA-256 hex digest)
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    # add more trusted config files here
}

def _compute_file_digest(filepath: str) -> str:
    """Return the SHA-256 hex digest of a file."""
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()

def apply_config_data(configuration_name: str, config_signature: str):
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        Name of the configuration file (relative to the current working directory).
    config_signature : str
        The expected cryptographic signature for the configuration file.

    Returns
    -------
    dict or None
        Parsed JSON configuration if signature verification succeeds, otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path and ensure file exists
    config_path = os.path.abspath(configuration_name)
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Compute the actual digest of the file
    try:
        actual_digest = _compute_file_digest(config_path)
    except Exception as exc:
        raise IOError(f"Failed to read configuration file '{configuration_name}': {exc}")

    # Compare signatures in a timing‑safe manner
    if not hmac.compare_digest(actual_digest, config_signature):
        # Signature mismatch; do not load the configuration
        return None

    # If signature matches, parse JSON safely
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise IOError(f"Failed to parse configuration file '{configuration_name}': {exc}")