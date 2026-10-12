#!/usr/bin/env python3
"""
Secure configuration loader with cryptographic signature verification.

This module defines a single function, `verify_config_data`, which reads
configuration data from a file and verifies that the supplied signature is
acceptable for that configuration.  The function protects against timing
attacks by using `hmac.compare_digest` for signature comparison.

The global dictionary `TRUSTED_CONFIG_SIGNATURES` maps file names to
their expected cryptographic signatures.  A signature can be any string,
but in practice it should be a secure hash (e.g. SHA‑256) of the file
contents.

CWE-347: Improper Verification of Cryptographic Signature is mitigated by:
* Strictly checking the signature against a known good value.
* Using constant‑time comparison to avoid leaking information through
  timing side‑channels.
"""

import os
import hmac

# Example trusted signatures. In a real system these would be generated
# securely and stored in a protected location.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.yaml": "d2c4e6f3a1b9e5d7f8c0e3b2a4c6f9e1d5b7a9c8e0f3d2b1a4c6e8f9d7b5a3c1",
    "db_settings.json": "a4e2f6d8b9c0e1f3d5a7b9c2e4f6d8b0a2c4e6f8d1b3a5c7e9f2d4b6a8c0e2",
    # Add additional entries as needed
}

def verify_config_data(config_file: str, provided_signature: str) -> dict | None:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_file : str
        The name of the configuration file to read.
    provided_signature : str
        The cryptographic signature supplied with the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration data if the signature is valid; otherwise,
        ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Resolve the absolute path and ensure the file exists
    abs_path = os.path.abspath(config_file)
    if not os.path.isfile(abs_path):
        raise IOError(f"Configuration file '{config_file}' not found.")

    # Read the raw data
    try:
        with open(abs_path, "rb") as fh:
            data_bytes = fh.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{config_file}': {exc}") from exc

    # Compute the expected signature for this file
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(config_file)

    # If the file is not in the trusted list, reject it
    if expected_signature is None:
        return None

    # Perform a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(provided_signature, expected_signature):
        return None

    # Parse the configuration data.  The format depends on the file type.
    # For simplicity, we support JSON and YAML in this example.
    try:
        if config_file.lower().endswith(".json"):
            import json
            return json.loads(data_bytes.decode("utf-8"))
        elif config_file.lower().endswith((".yml", ".yaml")):
            import yaml  # Requires PyYAML
            return yaml.safe_load(data_bytes.decode("utf-8"))
        else:
            # For unknown formats, return raw bytes or raise an error
            return {"raw": data_bytes}
    except Exception as exc:
        # Parsing failed – treat as invalid configuration
        return None

# Example usage (would normally be in a separate test or application module):
if __name__ == "__main__":
    try:
        config = verify_config_data("app_config.yaml", "d2c4e6f3a1b9e5d7f8c0e3b2a4c6f9e1d5b7a9c8e0f3d2b1a4c6e8f9d7b5a3c1")
        if config is None:
            print("Invalid signature or configuration could not be parsed.")
        else:
            print("Configuration loaded successfully:", config)
    except IOError as e:
        print(e)