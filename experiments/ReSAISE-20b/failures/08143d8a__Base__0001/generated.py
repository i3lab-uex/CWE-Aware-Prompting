#!/usr/bin/env python3
"""
Secure configuration file evaluator.

This module defines `evaluate_config_file`, which validates a cryptographic signature
against a trusted list before loading configuration data from a file.
"""

import json
import os
from typing import Dict, Optional

# Example trusted signatures mapping. In a real application this would be
# populated from a secure source (e.g., environment variable, secure vault,
# or hard‑coded constants).
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # signature : config_filename
    "a1b2c3d4e5f6g7h8i9j0": "app_config.json",
    "1234567890abcdef1234": "db_config.yaml",  # example
}

def _is_signature_trusted(provided_sig: str, config_filename: str) -> bool:
    """
    Internal helper to check if the provided signature is trusted for the
    requested configuration file.

    Args:
        provided_sig: The cryptographic signature supplied with the config.
        config_filename: The name of the configuration file.

    Returns:
        True if the signature is trusted for this file, False otherwise.
    """
    # Direct lookup: ensure that the provided signature maps to the expected file
    return TRUSTED_CONFIG_SIGNATURES.get(provided_sig) == config_filename


def evaluate_config_file(config_filename: str, provided_sig: str) -> Optional[Dict]:
    """
    Validate the cryptographic signature of a configuration file and load its
    contents if valid.

    Args:
        config_filename: Name of the configuration file to read.
        provided_sig: Cryptographic signature supplied alongside the config.

    Returns:
        A dictionary containing the parsed configuration data if the
        signature is valid; otherwise, None.

    Raises:
        IOError: If the requested configuration file does not exist or
                 cannot be read.
    """
    # 1. Verify that the file exists and is readable
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' not found.")

    # 2. Verify the signature
    if not _is_signature_trusted(provided_sig, config_filename):
        # Signature mismatch or untrusted
        return None

    # 3. Load the configuration file safely
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            # Support JSON; extendable to other formats if needed
            config_data = json.load(f)
    except Exception as exc:
        # Wrap any file or parsing errors in an IOError
        raise IOError(f"Failed to read configuration '{config_filename}': {exc}") from exc

    # 4. Return the parsed data
    return config_data


# Example usage (for testing purposes only; remove in production)
if __name__ == "__main__":
    # Assuming 'app_config.json' exists and has a trusted signature
    filename = "app_config.json"
    sig = TRUSTED_CONFIG_SIGNATURES.get(filename, "")
    try:
        cfg = evaluate_config_file(filename, sig)
        if cfg is not None:
            print("Configuration loaded successfully:", cfg)
        else:
            print("Invalid signature; configuration not loaded.")
    except IOError as e:
        print(f"Error: {e}")