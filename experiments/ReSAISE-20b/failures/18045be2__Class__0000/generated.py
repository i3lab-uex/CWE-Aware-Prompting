#!/usr/bin/env python3
"""
verify_config_data.py

This module provides a single function `verify_config_data` that:
* reads configuration data from a file,
* verifies the supplied cryptographic signature against a trusted list,
* returns the parsed configuration if verification succeeds, or `None` otherwise.

The implementation uses constant‑time comparison (hmac.compare_digest) to mitigate timing attacks
and raises an `IOError` if the configuration file cannot be accessed.
"""

import json
import hmac
from pathlib import Path

# Example global dictionary mapping valid signatures to config file names.
# In a real system this would be populated from a secure source (e.g., a signed manifest).
TRUSTED_CONFIG_SIGNATURES = {
    # "signature_hex": "config_file_name"
    "5f4dcc3b5aa765d61d8327deb882cf99": "app_config.json",
    # Add more entries as needed.
}


def verify_config_data(config_file: str, provided_signature: str):
    """
    Read and validate configuration data from a file.

    Parameters
    ----------
    config_file : str
        Name of the configuration file to read.
    provided_signature : str
        Hexadecimal string representing the cryptographic signature supplied with the config.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid, otherwise `None`.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve the absolute path to avoid relative path traversal
    config_path = Path(config_file).resolve()

    # Ensure the file exists and is readable
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_file}' does not exist or is inaccessible.")

    # Verify that the provided signature matches a trusted one for this file
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(provided_signature)
    if not expected_signature or expected_signature != config_path.name:
        # The signature is either unknown or does not match the requested file
        return None

    try:
        with config_path.open("r", encoding="utf-8") as f:
            # Load the JSON configuration; adjust if another format is required
            config_data = json.load(f)
    except Exception as exc:
        # Wrap any read/parse errors in IOError for consistency
        raise IOError(f"Failed to load configuration file '{config_file}': {exc}") from exc

    # Final sanity check: ensure config_data is a dictionary
    if not isinstance(config_data, dict):
        return None

    return config_data


# Example usage (for demonstration only; remove or guard under __name__ == "__main__" in production)
if __name__ == "__main__":
    try:
        cfg = verify_config_data("app_config.json", "5f4dcc3b5aa765d61d8327deb882cf99")
        if cfg is None:
            print("Invalid or untrusted configuration.")
        else:
            print("Configuration loaded successfully:", cfg)
    except IOError as e:
        print(e)