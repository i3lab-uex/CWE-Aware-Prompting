#!/usr/bin/env python3
"""
Utility for loading configuration files with signature verification.

The function `process_config_data` reads a JSON configuration file,
verifies its cryptographic signature against the trusted signatures
dictionary, and returns the parsed data as a dictionary.

The implementation uses `hmac.compare_digest` to mitigate timing attacks
(CWE‑693) and raises an `IOError` if the file cannot be located.
"""

import json
import os
from pathlib import Path
import hmac

# Global dictionary mapping config file names to trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; replace with actual file names and signatures.
    "app_config.json": "d2c3f8a1e9b4... (example signature)",
    # Add more trusted config signatures here.
}


def process_config_data(config_name: str, signature: str) -> dict | None:
    """
    Load and verify a configuration file.

    Parameters
    ----------
    config_name : str
        Name of the JSON configuration file to load.
    signature : str
        Cryptographic signature accompanying the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if signature matches the trusted
        value; otherwise, `None`.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path to avoid relative path attacks
    config_path = Path(config_name).resolve()

    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_name}' not found.")

    # Retrieve the trusted signature for this config
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if trusted_sig is None:
        # If we don't have a trusted signature, reject by default
        return None

    # Use constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(signature, trusted_sig):
        return None

    # Read and parse the JSON configuration
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Treat file read errors or invalid JSON as an IO error
        raise IOError(f"Failed to load configuration '{config_name}': {exc}") from exc

    return data