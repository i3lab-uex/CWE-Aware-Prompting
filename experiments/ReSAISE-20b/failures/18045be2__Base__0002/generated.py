#!/usr/bin/env python3
"""
Secure configuration loader with cryptographic signature verification.

The function `verify_config_data` reads a JSON configuration file, verifies that the
supplied signature matches the SHA‑256 hash of the file contents and that this
signature is present in a global whitelist (`TRUSTED_CONFIG_SIGNATURES`).  The
verification uses constant‑time comparison to mitigate timing attacks (CWE‑347).

Author: ChatGPT
"""

import json
import os
from hashlib import sha256
from hmac import compare_digest

# Global whitelist mapping *valid* signatures to their corresponding filenames.
# In a real deployment this would be stored securely (e.g., in an HSM or
# environment variable).  Here it is hard‑coded for demonstration purposes.
TRUSTED_CONFIG_SIGNATURES = {
    # Example: "<signature>": "config.json"
}

def verify_config_data(config_file: str, provided_signature: str) -> dict | None:
    """
    Load and verify a configuration file.

    Parameters
    ----------
    config_file : str
        Name of the JSON configuration file to load.
    provided_signature : str
        Cryptographic signature supplied alongside the configuration.

    Returns
    -------
    dict | None
        Parsed JSON content if the signature is valid; otherwise, ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    # Ensure the signature is a hex string of the expected length (64 chars for SHA‑256)
    if not isinstance(provided_signature, str) or len(provided_signature) != 64:
        return None

    # Resolve the absolute path and check existence
    config_path = os.path.abspath(config_file)
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{config_file}' not found")

    # Read the file in binary mode to compute its hash accurately
    with open(config_path, "rb") as f:
        content = f.read()

    # Compute SHA‑256 hash of the file contents
    computed_hash = sha256(content).hexdigest()

    # Verify that the provided signature matches the computed hash
    if not compare_digest(computed_hash, provided_signature):
        return None

    # Ensure the signature is in the trusted whitelist and maps to this file
    expected_file = TRUSTED_CONFIG_SIGNATURES.get(provided_signature)
    if expected_file is None or os.path.normpath(expected_file) != os.path.normpath(config_file):
        return None

    # Parse JSON content safely
    try:
        config_data = json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    return config_data