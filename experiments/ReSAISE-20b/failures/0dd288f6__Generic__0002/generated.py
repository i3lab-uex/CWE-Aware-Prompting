import json
import os
import hashlib
import hmac

# Global dictionary mapping configuration filenames to their expected signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – replace with real values in production
    "app_config.json": "5f4dcc3b5aa765d61d8327deb882cf99",
    "db_config.json":  "e99a18c428cb38d5f260853678922e03",
}

def _compute_file_signature(file_path: str) -> str:
    """
    Compute the SHA-256 hex digest of a file's contents.
    """
    hash_obj = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def apply_config_data(configuration_name: str, config_signature: str) -> dict | None:
    """
    Load and validate a configuration file.

    Parameters
    ----------
    configuration_name : str
        Name of the configuration file (relative to current working directory).
    config_signature : str
        Cryptographic signature supplied for verification.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature matches, otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be located.
    """
    # Resolve absolute path and ensure the file exists
    config_path = os.path.abspath(configuration_name)
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{configuration_name}' not found.")

    # Compute the signature of the file
    actual_signature = _compute_file_signature(config_path)

    # Retrieve expected signature from the trusted dictionary
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(configuration_name)

    # If there is no trusted signature for this file, reject it
    if expected_signature is None:
        return None

    # Constant‑time comparison to prevent timing attacks
    if not hmac.compare_digest(actual_signature, expected_signature):
        return None

    # The signature matches – parse the configuration
    with open(config_path, "r", encoding="utf-8") as f:
        try:
            config_data = json.load(f)
        except json.JSONDecodeError:
            # Invalid JSON – treat as untrusted
            return None

    return config_data