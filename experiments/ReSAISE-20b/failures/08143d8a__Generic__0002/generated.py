#!/usr/bin/env python3
"""
Utility to load a configuration file only if it is accompanied by an approved cryptographic signature.
"""

import json
import os

# Example global mapping of valid signatures to configuration filenames.
# In a real system this would be populated from a secure source or environment variable.
TRUSTED_CONFIG_SIGNATURES = {
    "f7a8b6e9c4d1e3a2b5f0": "app_settings.json",
    "9c8d7e6f5a4b3c2d1e0f": "db_config.yaml",
    # Add more trusted signatures here
}


def evaluate_config_file(config_filename: str, provided_sig: str) -> dict | None:
    """
    Load and validate a configuration file.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    provided_sig : str
        Cryptographic signature supplied alongside the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration data if signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file cannot be found or read.
    """
    # Verify that the provided signature matches the expected one for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if not expected_sig:
        # No trusted signature registered for this file
        return None

    if provided_sig != expected_sig:
        # Signature mismatch – do not load the file
        return None

    # Resolve the absolute path to prevent directory traversal attacks
    safe_path = os.path.abspath(config_filename)

    if not os.path.isfile(safe_path):
        raise IOError(f"Configuration file '{config_filename}' not found.")

    try:
        with open(safe_path, "r", encoding="utf-8") as fp:
            content = fp.read()
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{config_filename}': {exc}") from exc

    # Attempt to parse the content as JSON; fallback to YAML if available
    try:
        config_data = json.loads(content)
    except json.JSONDecodeError:
        # If JSON fails, try YAML parsing if PyYAML is installed
        try:
            import yaml  # type: ignore
        except ImportError:
            raise ValueError(
                f"Configuration file '{config_filename}' is not valid JSON and PyYAML is not installed."
            )
        config_data = yaml.safe_load(content)

    if not isinstance(config_data, dict):
        raise ValueError(f"Configuration file '{config_filename}' does not contain a JSON/YAML object.")

    return config_data