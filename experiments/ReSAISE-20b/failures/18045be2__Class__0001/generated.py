#!/usr/bin/env python3
"""
Utility to load a configuration file only if its cryptographic signature is trusted.
"""

import json
from pathlib import Path
from typing import Dict, Optional

# Global dictionary mapping trusted signatures to configuration file names.
# In a real system this would be populated from a secure source (e.g.,
# environment variables, a signed manifest, etc.).
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # Example entries:
    # "sha256-signature-of-config1.json": "config1.json",
    # "sha256-signature-of-config2.json": "config2.json",
}

def verify_config_data(config_file: str, provided_signature: str) -> Optional[Dict]:
    """
    Load and return the configuration data from *config_file* if
    *provided_signature* is a trusted signature for that file.

    Parameters:
        config_file (str): The name of the configuration file to load.
        provided_signature (str): The cryptographic signature accompanying
            the configuration data.

    Returns:
        dict: Parsed JSON configuration if the signature is valid.
        None: If the signature does not match any trusted entry.

    Raises:
        IOError: If *config_file* cannot be found or read.
    """
    # Resolve the file path safely
    config_path = Path(config_file).expanduser().resolve()

    # Ensure the file exists before attempting to read it
    if not config_path.is_file():
        raise IOError(f"Configuration file '{config_file}' not found.")

    # Verify the signature against the trusted list
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(provided_signature)
    if expected_file != config_path.name:
        # Signature does not match the file; reject
        return None

    # Read and parse the JSON configuration
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Treat file read or parse errors as an I/O error
        raise IOError(f"Failed to load configuration from '{config_file}': {exc}") from exc

    return data