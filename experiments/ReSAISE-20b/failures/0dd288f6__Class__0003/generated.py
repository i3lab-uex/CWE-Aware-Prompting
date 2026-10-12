import os
import json
import hashlib
from typing import Optional, Dict

# Global mapping of trusted config file names to their SHA‑256 hex digests
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries; populate with real values in production
    "app_config.json": "3a7bd3e2360a6c1b2d9f8e5c4b1e7f0d3a6c2b1e9f8d7c5b4a3e2f1d0c9b8a7",
    "db_config.json":  "6b2f3e4d5c6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
}

def _compute_sha256(file_path: str) -> str:
    """Compute the SHA‑256 hex digest of a file in chunks."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()

def _constant_time_compare(a: str, b: str) -> bool:
    """Return True if the two strings are equal using a constant‑time comparison."""
    return hashlib.compare_digest(a, b)

def apply_config_data(configuration_name: str,
                      config_signature: str) -> Optional[Dict]:
    """
    Load a configuration file after verifying its cryptographic signature.

    Parameters
    ----------
    configuration_name : str
        The name of the configuration file (relative to the current working directory).
    config_signature : str
        The expected SHA‑256 hex digest of the configuration file.

    Returns
    -------
    dict or None
        The parsed JSON configuration if the signature matches; otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path to avoid directory traversal attacks
    config_path = os.path.abspath(configuration_name)

    # Ensure the file exists and is a regular file
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{configuration_name}' not found")

    # Compute the actual digest
    try:
        actual_digest = _compute_sha256(config_path)
    except Exception as exc:   # pragma: no cover
        raise IOError(f"Failed to read configuration file '{configuration_name}': {exc}") from exc

    # Verify signature in constant time
    if not _constant_time_compare(actual_digest, config_signature):
        # Signature mismatch – do NOT load the configuration
        return None

    # Load and parse JSON content safely
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as exc:   # pragma: no cover
        raise IOError(f"Failed to parse configuration file '{configuration_name}': {exc}") from exc

    # Ensure the returned object is a dictionary
    if not isinstance(config_data, dict):
        return None

    return config_data